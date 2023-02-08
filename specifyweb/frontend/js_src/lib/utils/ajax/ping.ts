import type { PartialBy } from '../types';
import { ajax } from './index';

/**
 * A wrapper for "ajax" for when response data is not needed
 *
 * @returns Response code
 * @throws Rejects promise on errors
 */
export const ping = async (
  url: string,
  options?: PartialBy<Parameters<typeof ajax>[1], 'headers'>,
  additionalOptions?: Parameters<typeof ajax>[2]
): Promise<number> =>
  ajax<never>(
    url,
    {
      ...options,
      headers: options?.headers ?? {},
    },
    additionalOptions
  ).then(({ status }) => status);
