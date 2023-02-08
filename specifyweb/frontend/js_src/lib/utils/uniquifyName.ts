import type { LocalizedString } from 'typesafe-i18n';

import type { DatasetBrief } from '../components/WbPlanView/Wrapped';
import { ajax } from './ajax';
import { f } from './functools';
import type { RA } from './types';
import { filterArray } from './types';
import { escapeRegExp } from './utils';

const MAX_NAME_LENGTH = 64;

export function getUniqueName(
  name: string,
  usedNames: RA<string>,
  /**
   * In the process of making the name unique, its length may increase.
   * This trims the string if needed, while still keeping it unique
   *
   * @remarks
   * Can get this number from SQL schema for a given field
   */
  maxLength: number = Number.POSITIVE_INFINITY
): LocalizedString {
  if (!usedNames.includes(name)) return name as LocalizedString;
  // FEATURE: allow customizing this?
  const suffix = / \((\d+)\)$/u.exec(name);
  const [{ length }, indexString] = suffix ?? ([[], '0'] as const);
  const strippedName = length > 0 ? name.slice(0, -1 * length) : name;
  const indexRegex = new RegExp(
    `^${escapeRegExp(strippedName)} \\((\\d+)\\)$`,
    'u'
  );
  const newIndex =
    Math.max(
      ...filterArray([
        f.parseInt(indexString),
        ...usedNames.map((name) => f.parseInt(indexRegex.exec(name)?.[1]) ?? 1),
      ])
    ) + 1;
  const uniquePart = ` (${newIndex})`;
  const newName =
    newIndex === 1 && length === 0
      ? strippedName
      : `${strippedName}${uniquePart}`;
  return newName.length > maxLength
    ? getUniqueName(name.slice(0, -1 * uniquePart.length), usedNames, maxLength)
    : (newName as LocalizedString);
}

export async function uniquifyDataSetName(
  name: string,
  currentDataSetId?: number
): Promise<string> {
  return ajax<RA<DatasetBrief>>(`/api/workbench/dataset/`, {
    headers: { Accept: 'application/json' },
  }).then(({ data: datasets }) =>
    getUniqueName(
      name,
      datasets
        .filter(({ id }) => id !== currentDataSetId)
        .map(({ name }) => name),
      MAX_NAME_LENGTH
    )
  );
}
