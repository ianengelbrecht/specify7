import type { IR, RA } from './components/wbplanview';
import lifemapperText from './localization/lifemapper';

const IS_DEVELOPMENT = false;

const defaultGuid = [
  '2c1becd5-e641-4e83-b3f5-76a55206539a',
  'dcb298f9-1ed3-11e3-bfac-90b11c41863e',
  '8eb23b1e-582e-4943-9dd9-e3a36ceeb498',
][0];
const defaultOccurrenceNames: Readonly<[string, string]> = [
  'Phlox longifolia Nutt.',
  'Phlox longifolia Nutt.',
] as const;

export const resolveGuid = (originalGuid: string): string =>
  IS_DEVELOPMENT ? defaultGuid : originalGuid;
export const resolveOccurrenceNames = (
  occurrenceNames: Readonly<[string, string]>
): Readonly<[string, string]> =>
  IS_DEVELOPMENT ? defaultOccurrenceNames : occurrenceNames;

export const snServer = 'https://broker-dev.spcoco.org';
export const snFrontendServer = 'https://broker.spcoco.org';

export const SN_SERVICES: IR<string> = {
  lm: lifemapperText('speciesDistributionMap'),
  sn: lifemapperText('specifyNetwork'),
};
export const ignoredAggregators: RA<string> = ['specify'];
export type MessageTypes = 'errorDetails' | 'infoSection';
