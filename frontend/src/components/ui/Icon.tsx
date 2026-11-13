import type { SVGProps } from 'react'

/**
 * Minimal in-house stroke icon set (24×24 grid) — avoids pulling an icon
 * library for a handful of glyphs.
 */
const paths = {
  overview: 'M4 13h6V4H4v9Zm10 7h6V11h-6v9ZM4 20h6v-4H4v4Zm10-13h6V4h-6v3Z',
  truck:
    'M3 6h11v9H3zM14 9h4l3 3.5V15h-7M7.5 18.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm10 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z',
  map: 'M9 4 3 6.5v13.5L9 17.5l6 2.5 6-2.5V4l-6 2.5L9 4Zm0 0v13.5m6-11v13.5',
  box: 'm12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Zm0 9 8-4.5M12 12 4 7.5M12 12v9',
  alert: 'M12 4 2.8 20h18.4L12 4Zm0 6v4.5m0 2.8v.2',
  sparkles:
    'M12 3.5 13.9 9l5.6 2-5.6 2L12 18.5 10.1 13l-5.6-2 5.6-2L12 3.5ZM19 3v3m-1.5-1.5h3M5 17.5v3M3.5 19h3',
  settings:
    'M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm7.4-3a7.4 7.4 0 0 0-.1-1.3l2-1.6-2-3.4-2.4 1a7.5 7.5 0 0 0-2.2-1.3L14.4 3h-4l-.4 2.4a7.5 7.5 0 0 0-2.2 1.3l-2.4-1-2 3.4 2 1.6a7.4 7.4 0 0 0 0 2.6l-2 1.6 2 3.4 2.4-1a7.5 7.5 0 0 0 2.2 1.3l.4 2.4h4l.4-2.4a7.5 7.5 0 0 0 2.2-1.3l2.4 1 2-3.4-2-1.6c.1-.4.1-.9.1-1.3Z',
  bell: 'M6 16V11a6 6 0 1 1 12 0v5l1.5 2h-15L6 16Zm4 4.5a2 2 0 0 0 4 0',
  search: 'M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14Zm9 2-4-4',
  menu: 'M4 7h16M4 12h16M4 17h16',
  close: 'M6 6l12 12M18 6 6 18',
  chevronDown: 'm6 9 6 6 6-6',
  arrowRight: 'M5 12h14m-5-5 5 5-5 5',
  arrowUpRight: 'M7 17 17 7M9 7h8v8',
  arrowDownRight: 'M7 7l10 10m0-8v8H9',
  check: 'M5 12.5 10 17 19 7.5',
  clock: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-13v4.5l3 2',
  pin: 'M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12Zm0-9.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
  info: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-10v5.5m0-8.3v.3',
  construction: 'M4 20h16M6 20V9l6-5 6 5v11M10 20v-6h4v6',
} as const

export type IconName = keyof typeof paths

interface IconProps extends Omit<SVGProps<SVGSVGElement>, 'name'> {
  name: IconName
  size?: number
}

export function Icon({ name, size = 20, strokeWidth = 1.75, ...rest }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      {...rest}
    >
      <path d={paths[name]} />
    </svg>
  )
}
