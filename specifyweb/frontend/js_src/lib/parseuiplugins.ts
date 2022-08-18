/**
 * Parse cell XML with a plugin definition into a JSON structure
 */

import type { State } from 'typesafe-reducer';

import type { PartialDatePrecision } from './components/partialdateui';
import { f } from './functools';
import { parseRelativeDate } from './relativedate';
import { CoordinateType, coordinateType } from './components/latlongui';

export type UiPlugins = {
  readonly LatLonUI: State<
    'LatLonUI',
    {
      readonly step: number | undefined;
      readonly latLongType: CoordinateType;
    }
  >;
  readonly PartialDateUI: State<
    'PartialDateUI',
    {
      readonly dateField: string | undefined;
      readonly defaultValue: Date | undefined;
      readonly precisionField: string | undefined;
      readonly defaultPrecision: PartialDatePrecision;
    }
  >;
  readonly CollectionRelOneToManyPlugin: State<
    'CollectionRelOneToManyPlugin',
    {
      readonly relationship: string | undefined;
    }
  >;
  readonly ColRelTypePlugin: State<
    'ColRelTypePlugin',
    {
      readonly relationship: string | undefined;
    }
  >;
  readonly LocalityGeoRef: State<'LocalityGeoRef'>;
  readonly WebLinkButton: State<
    'WebLinkButton',
    {
      readonly webLink: string | undefined;
      readonly icon: string;
    }
  >;
  readonly AttachmentPlugin: State<'AttachmentPlugin'>;
  readonly HostTaxonPlugin: State<
    'HostTaxonPlugin',
    {
      readonly relationship: string | undefined;
    }
  >;
  readonly LocalityGoogleEarth: State<'LocalityGoogleEarth'>;
  readonly PaleoMap: State<'PaleoMap'>;
  readonly Unsupported: State<
    'Unsupported',
    {
      readonly name: string | undefined;
    }
  >;
};

const processUiPlugin: {
  readonly [KEY in keyof UiPlugins]: (props: {
    readonly getProperty: (name: string) => string | undefined;
    readonly defaultValue: string | undefined;
  }) => UiPlugins[KEY];
} = {
  LatLonUI({ getProperty }) {
    const latLongType = getProperty('latLongType') ?? '';
    return {
      type: 'LatLonUI',
      step: f.parseInt(getProperty('step') ?? ''),
      latLongType:
        coordinateType.find(
          (type) => type.toLowerCase() === latLongType.toLowerCase()
        ) ?? 'Point',
    };
  },
  PartialDateUI: ({ getProperty, defaultValue }) => ({
    type: 'PartialDateUI',
    defaultValue: f.maybe(
      defaultValue?.trim().toLowerCase(),
      parseRelativeDate
    ),
    dateField: getProperty('df')?.toLowerCase(),
    precisionField: getProperty('tp')?.toLowerCase(),
    defaultPrecision: f.var(
      getProperty('defaultPrecision')?.toLowerCase(),
      (defaultPrecision) =>
        f.includes(['year', 'month-year'], defaultPrecision)
          ? (defaultPrecision as 'year' | 'month-year')
          : 'full'
    ),
  }),
  CollectionRelOneToManyPlugin: ({ getProperty }) => ({
    type: 'CollectionRelOneToManyPlugin',
    relationship: getProperty('relName'),
  }),
  // Collection one-to-one Relationship plugin
  ColRelTypePlugin: ({ getProperty }) => ({
    type: 'ColRelTypePlugin',
    relationship: getProperty('relName'),
  }),
  LocalityGeoRef: () => ({ type: 'LocalityGeoRef' }),
  WebLinkButton: ({ getProperty }) => ({
    type: 'WebLinkButton',
    webLink: getProperty('webLink'),
    icon: getProperty('icon') ?? 'WebLink',
  }),
  AttachmentPlugin: () => ({ type: 'AttachmentPlugin' }),
  HostTaxonPlugin: ({ getProperty }) => ({
    type: 'HostTaxonPlugin',
    relationship: getProperty('relName'),
  }),
  LocalityGoogleEarth: () => ({ type: 'LocalityGoogleEarth' }),
  PaleoMap: () => ({ type: 'PaleoMap' }),
  Unsupported: ({ getProperty }) => ({
    type: 'Unsupported',
    name: getProperty('name'),
  }),
};

export type PluginDefinition = UiPlugins[keyof UiPlugins];

export function parseUiPlugin(
  getProperty: (name: string) => string | undefined,
  defaultValue: string | undefined
): PluginDefinition {
  const uiCommand =
    processUiPlugin[(getProperty('name') ?? '') as keyof UiPlugins] ??
    processUiPlugin.Unsupported;
  return uiCommand({ getProperty, defaultValue });
}
