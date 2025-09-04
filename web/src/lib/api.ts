export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
    const res = await fetch(`/api${path}`, {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...(init.headers || {}),
        },
        ...init,
    })

    if (!res.ok) {
        const text = await res.text().catch(() => '')
        throw new Error(text || `HTTP ${res.status}`)
    }

    try {
        return (await res.json()) as T
    } catch {
        return {} as T
    }
}