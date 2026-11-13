const numberFormatter = new Intl.NumberFormat('fr-FR')

export function formatNumber(value: number): string {
  return numberFormatter.format(value)
}

const dateTimeFormatter = new Intl.DateTimeFormat('fr-FR', {
  day: '2-digit',
  month: 'short',
  hour: '2-digit',
  minute: '2-digit',
})

export function formatDateTime(iso: string): string {
  return dateTimeFormatter.format(new Date(iso))
}

/** Joins conditional class names. */
export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(' ')
}
