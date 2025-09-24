export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
    const headers = new Headers(init.headers || {})
    const isForm =
        init.body instanceof URLSearchParams ||
        (typeof FormData !== 'undefined' && init.body instanceof FormData)

    if (!headers.has('Content-Type') && !isForm) {
        headers.set('Content-Type', 'application/json')
    }

    let body = init.body as BodyInit | undefined
    if (
        headers.get('Content-Type')?.includes('application/json') &&
        body &&
        typeof body === 'object' &&
        !isForm
    ) {
        body = JSON.stringify(body)
    }

    const res = await fetch(`/api${path}`, {
        credentials: 'include',
        ...init,
        headers,
        body,
    })

    if (!res.ok) {
        const ct = res.headers.get('Content-Type') || ''
        const err = ct.includes('application/json')
            ? await res.json().catch(() => null)
            : await res.text().catch(() => '')
        throw new Error(err ? JSON.stringify(err) : `HTTP ${res.status}`)
    }

    const ct = res.headers.get('Content-Type') || ''
    return ct.includes('application/json') ? ((await res.json()) as T) : ({} as T)
}
