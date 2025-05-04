export function cn(...inputs: (string | undefined | false)[]) {
    return inputs.filter(Boolean).join(' ')
}

export function formatDate(dateString: string) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    })
}
