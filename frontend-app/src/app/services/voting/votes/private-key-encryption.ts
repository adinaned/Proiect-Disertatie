export async function encryptPrivateKey(privateKey: string, password: string): Promise<string> {
    const encoder = new TextEncoder();
    const keyMaterial = await window.crypto.subtle.importKey(
        'raw',
        encoder.encode(password),
        { name: 'PBKDF2' },
        false,
        ['deriveKey']
    );

    const salt = window.crypto.getRandomValues(new Uint8Array(16));
    const key = await window.crypto.subtle.deriveKey(
        {
            name: 'PBKDF2',
            salt: salt,
            iterations: 100_000,
            hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-GCM', length: 256 },
        true,
        ['encrypt']
    );

    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const encrypted = await window.crypto.subtle.encrypt(
        {
            name: 'AES-GCM',
            iv: iv
        },
        key,
        encoder.encode(privateKey)
    );

    return btoa(
        JSON.stringify({
            salt: Array.from(salt),
            iv: Array.from(iv),
            data: Array.from(new Uint8Array(encrypted))
        })
    );
}


export async function decryptPrivateKey(encryptedData: string, password: string): Promise<string> {
    const data = Uint8Array.from(atob(encryptedData), c => c.charCodeAt(0));

    const salt = data.slice(0, 16);
    const iv = data.slice(16, 28);
    const ciphertext = data.slice(28);

    const keyMaterial = await getKeyMaterial(password);
    const key = await deriveKey(keyMaterial, salt);

    const decrypted = await crypto.subtle.decrypt(
        {name: "AES-GCM", iv},
        key,
        ciphertext
    );

    return new TextDecoder().decode(decrypted);
}

async function getKeyMaterial(password: string): Promise<CryptoKey> {
    return crypto.subtle.importKey(
        "raw",
        new TextEncoder().encode(password),
        {name: "PBKDF2"},
        false,
        ["deriveKey"]
    );
}

async function deriveKey(keyMaterial: CryptoKey, salt: Uint8Array): Promise<CryptoKey> {
    return crypto.subtle.deriveKey(
        {
            name: "PBKDF2",
            salt,
            iterations: 100_000,
            hash: "SHA-256"
        },
        keyMaterial,
        {name: "AES-GCM", length: 256},
        false,
        ["encrypt", "decrypt"]
    );
}
