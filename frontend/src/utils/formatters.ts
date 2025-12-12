/**
 * Format a number as currency with commas and 2 decimal places
 * @param value - The number to format
 * @param currency - The currency code (default: USD)
 * @returns Formatted string like "$1,999.99"
 */
export function formatCurrency(value: number | null | undefined, currency: string = 'USD'): string {
  if (value === null || value === undefined) {
    return 'N/A'
  }
  
  return value.toLocaleString('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
}

/**
 * Format a number with commas (no currency symbol)
 * @param value - The number to format
 * @returns Formatted string like "1,999.99"
 */
export function formatNumber(value: number | null | undefined, decimals: number = 2): string {
  if (value === null || value === undefined) {
    return 'N/A'
  }
  
  return value.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  })
}

/**
 * Get the currency symbol for a given currency code
 * @param currency - The currency code (e.g., 'USD', 'EUR', 'GBP')
 * @returns The currency symbol (e.g., '$', '€', '£')
 */
export function getCurrencySymbol(currency: string = 'USD'): string {
  try {
    // Use Intl.NumberFormat to get the currency symbol for any currency
    const formatted = (0).toLocaleString('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    })
    // Extract just the symbol (removes the '0')
    return formatted.replace('0', '').trim()
  } catch {
    // Fallback if currency code is invalid
    return '$'
  }
}


