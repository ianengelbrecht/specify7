/**
 * Collection of various helper methods used during the mapping process
 *
 * @module
 */

import type { IR, RA, RR } from './types';
import type { SplitMappingPath } from './wbplanviewmappinghelper';

export const capitalize = <T extends string>(string: T): Capitalize<T> =>
  (string.charAt(0).toUpperCase() + string.slice(1)) as Capitalize<T>;

export const unCapitalize = <T extends string>(string: T): Uncapitalize<T> =>
  (string.charAt(0).toLowerCase() + string.slice(1)) as Uncapitalize<T>;

/** Type-safe variant of toLowerCase */
export const toLowerCase = <T extends string>(string: T): Lowercase<T> =>
  string.toLowerCase() as Lowercase<T>;

/**
 * Finds the point at which the source array begins to have values
 * different from the ones in the search array
 *
 * @example
 * Returns 0 if search array is empty
 * Returns -1 if source array is empty / is shorter than the search array
 * Examples:
 *   If:
 *     source is ['Accession','Accession Agents','#1','Agent','First Name'] and
 *     search is []
 *   returns 0
 *   If:
 *     source is ['Accession','Accession Agents','#1','Agent','First Name'] and
 *     search is ['Accession','Accession Agents',]
 *   returns 2
 *   If
 *     source is ['Accession','Accession Agents','#1','Agent','First Name'] and
 *     search is ['Accession','Accession Agents','#2']
 *   returns -1
 *
 */
export function findArrayDivergencePoint<T>(
  // The source array to use in the comparison
  source: RA<T>,
  // The search array to use in the comparison
  search: RA<T>
): number {
  if (source === null || search === null) return -1;

  const sourceLength = source.length;
  const searchLength = search.length;

  if (searchLength === 0) return 0;

  if (sourceLength === 0 || sourceLength < searchLength) return -1;

  return (
    mappedFind(Object.entries(source), ([index, sourceValue]) => {
      const searchValue = search[Number(index)];

      if (typeof searchValue === 'undefined') return Number(index);
      else if (sourceValue === searchValue) return undefined;
      else return -1;
    }) ?? searchLength - 1
  );
}

export const extractDefaultValues = (
  splitMappingPaths: RA<SplitMappingPath>,
  emptyStringReplacement = ''
): IR<string> =>
  Object.fromEntries(
    splitMappingPaths
      .map(
        ({ headerName, columnOptions }) =>
          [
            headerName,
            columnOptions.default === ''
              ? emptyStringReplacement
              : columnOptions.default,
          ] as [string, string]
      )
      .filter(([, defaultValue]) => defaultValue !== null)
  );

export const upperToKebab = (value: string): string =>
  value.toLowerCase().split('_').join('-');

export const camelToKebab = (value: string): string =>
  value.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();

export const camelToHuman = (value: string): string =>
  capitalize(value.replace(/([a-z])([A-Z])/g, '$1 $2')).replace(/Dna\b/, 'DNA');

/** Scale a number from original range into new range */
export const spanNumber =
  (
    minInput: number,
    maxInput: number,
    minOutput: number,
    maxOutput: number
  ): ((input: number) => number) =>
  (input: number): number =>
    ((input - minInput) / (maxInput - minInput)) * (maxOutput - minOutput) +
    minOutput;

/** Get Dictionary's key in a case insensitive way */
export const caseInsensitiveHash = <
  KEY extends string,
  DICTIONARY extends RR<KEY, unknown>
>(
  dictionary: DICTIONARY,
  searchKey:
    | KEY
    | Lowercase<KEY>
    | Uppercase<KEY>
    | Capitalize<KEY>
    | Uncapitalize<KEY>
): DICTIONARY[KEY] =>
  Object.entries(dictionary).find(
    ([key]) => key.toLowerCase() === searchKey.toLowerCase()
  )?.[1] as DICTIONARY[KEY];

/** Generate a sort function for Array.prototype.sort */
export const sortFunction = <T, V extends boolean | number>(
  mapper: (value: T) => V,
  reverse = false
): ((left: T, right: T) => -1 | 0 | 1) =>
  reverse
    ? (left: T, right: T): -1 | 0 | 1 =>
        mapper(left) < mapper(right)
          ? -1
          : mapper(left) === mapper(right)
          ? 0
          : 1
    : (left: T, right: T): -1 | 0 | 1 =>
        mapper(left) > mapper(right)
          ? 1
          : mapper(left) === mapper(right)
          ? 0
          : -1;

/** Split array in half according to a discriminator function */
export const split = <ITEM>(
  array: RA<ITEM>,
  discriminator: (item: ITEM, index: number) => boolean
): Readonly<[left: RA<ITEM>, right: RA<ITEM>]> =>
  array
    .map((item, index) => [item, discriminator(item, index)] as const)
    .reduce<Readonly<[left: RA<ITEM>, right: RA<ITEM>]>>(
      ([left, right], [item, isRight]) => [
        [...left, ...(isRight ? [] : [item])],
        [...right, ...(isRight ? [item] : [])],
      ],
      [[], []]
    );

/** Convert an array of [key,value] tuples to a Dict[key, value[]]*/
export const group = <KEY extends PropertyKey, VALUE>(
  entries: RA<Readonly<[key: KEY, value: VALUE]>>
): RR<KEY, RA<VALUE>> =>
  entries.reduce<RR<KEY, RA<VALUE>>>(
    (grouped, [key, value]) => ({
      ...grouped,
      [key]: [...(grouped[key] ?? []), value],
    }),
    {}
  );

// Find a value in an array, and return it's mapped variant
export function mappedFind<ITEM, RETURN_TYPE>(
  array: RA<ITEM>,
  callback: (item: ITEM, index: number) => RETURN_TYPE | undefined
): RETURN_TYPE | undefined {
  let value = undefined;
  array.some((item, index) => {
    value = callback(item, index);
    return typeof value !== 'undefined';
  });
  return value;
}
