import React from 'react';

import type { Locality } from '../datamodel';
import { Lat, Long } from '../latlongutils';
import type { SpecifyResource } from '../legacytypes';
import { commonText } from '../localization/common';
import { localityText } from '../localization/locality';
import type { FormMode } from '../parseform';
import { resourceOn } from '../resource';
import { Input, Select } from './basic';

export const coordinateType = ['Point', 'Line', 'Rectangle'] as const;
export type CoordinateType = typeof coordinateType[number];

type Parsed = {
  readonly format: (step: number | undefined) => string;
  readonly asFloat: () => number;
  readonly soCalledUnit: () => number;
};

function Coordinate({
  resource,
  coordinateField,
  coordinateTextField,
  fieldType,
  isReadOnly,
  onChange: handleChange,
  step,
}: {
  readonly resource: SpecifyResource<Locality>;
  readonly coordinateField: `${'latitude' | 'longitude'}${1 | 2}`;
  readonly coordinateTextField: `${'lat' | 'long'}${1 | 2}text`;
  readonly fieldType: 'Lat' | 'Long';
  readonly isReadOnly: boolean;
  readonly onChange: (parsed: string) => void;
  readonly step: number | undefined;
}): JSX.Element {
  const [coordinate, setCoordinate] = React.useState<string>(
    () =>
      (resource.get(coordinateTextField) ||
        resource.get(coordinateField)?.toString()) ??
      ''
  );

  const handleChanged = (raw: string, formatted: string | undefined) =>
    handleChange(raw === '' ? commonText('notApplicable') : formatted ?? '???');

  React.useEffect(() => {
    const handleChange = (coordinate: string): void =>
      handleChanged(
        coordinate,
        (
          (fieldType === 'Lat' ? Lat : Long).parse(coordinate) as Parsed | null
        )?.format(step)
      );
    const textDestructor = resourceOn(
      resource,
      `change:${coordinateTextField}`,
      (): void => {
        setCoordinate(
          resource.get(coordinateTextField) ??
            resource.get(coordinateField)?.toString() ??
            ''
        );
        handleChange(
          resource.get(coordinateTextField) ?? resource.get(coordinateField)
        );
      },
      // Update parent's Preview column with initial values on first render
      true
    );
    const destructor = resourceOn(
      resource,
      `change:${coordinateField}`,
      (): void => handleChange(resource.get(coordinateField)?.toString() ?? '')
    );

    return (): void => {
      textDestructor();
      destructor();
    };
  }, [resource, step, coordinateField, coordinateTextField, fieldType]);

  return (
    <Input.Text
      value={coordinate}
      isReadOnly={isReadOnly}
      onValueChange={(value): void => {
        setCoordinate(value);
        const hasValue = value.trim() !== '';
        const parsed = hasValue
          ? (((fieldType === 'Lat' ? Lat : Long).parse(value) ?? undefined) as
              | Parsed
              | undefined)
          : undefined;
        handleChanged(value.trim(), parsed?.format(step));

        resource.set(coordinateTextField, value);
        resource.set(coordinateField, parsed?.asFloat() ?? null);
        resource.set('srcLatLongUnit', parsed?.soCalledUnit() ?? 3);
        resource.set('originalLatLongUnit', parsed?.soCalledUnit() ?? null);
      }}
    />
  );
}

function CoordinatePoint({
  resource,
  label,
  index,
  isReadOnly,
  step,
}: {
  readonly resource: SpecifyResource<Locality>;
  readonly label: string;
  readonly index: 1 | 2;
  readonly isReadOnly: boolean;
  readonly step: number | undefined;
}): JSX.Element {
  const [latitude, setLatitude] = React.useState<string>(
    commonText('notApplicable')
  );
  const [longitude, setLongitude] = React.useState<string>(
    commonText('notApplicable')
  );
  return (
    <tr>
      <th scope="row">{label}</th>
      <td>
        <label>
          <span className="sr-only">{`${localityText(
            'latitude'
          )} ${index}`}</span>
          <Coordinate
            resource={resource}
            coordinateField={`latitude${index}`}
            coordinateTextField={`lat${index}text`}
            fieldType={`Lat`}
            isReadOnly={isReadOnly}
            onChange={setLatitude}
            step={step}
          />
        </label>
      </td>
      <td>
        <label>
          <span className="sr-only">{`${localityText(
            'longitude'
          )} ${index}`}</span>
          <Coordinate
            resource={resource}
            coordinateField={`longitude${index}`}
            coordinateTextField={`long${index}text`}
            fieldType={`Long`}
            isReadOnly={isReadOnly}
            onChange={setLongitude}
            step={step}
          />
        </label>
      </td>
      <td>
        <span>{latitude}</span>
        {', '}
        <span>{longitude}</span>
      </td>
    </tr>
  );
}

export function LatLongUi({
  resource,
  mode,
  id,
  step,
  latLongType,
}: {
  readonly resource: SpecifyResource<Locality>;
  readonly mode: FormMode;
  readonly id: string | undefined;
  readonly step: number | undefined;
  readonly latLongType: CoordinateType;
}): JSX.Element {
  const [coordinateType, setCoordinateType] = React.useState<CoordinateType>(
    () => resource.get('latLongType') ?? latLongType
  );

  React.useEffect(
    () =>
      resourceOn(resource, 'change:latLongType', (): void =>
        setCoordinateType(
          // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
          (resource.get('latLongType') as CoordinateType) ?? 'Point'
        )
      ),
    [resource]
  );

  return (
    <fieldset>
      <table className="w-full text-center">
        <thead>
          <tr>
            <th scope="col">
              <label>
                <span className="sr-only">
                  {localityText('coordinateType')}
                </span>
                <Select
                  id={id}
                  name="type"
                  title={localityText('coordinateType')}
                  value={coordinateType}
                  disabled={mode === 'view'}
                  onValueChange={(value): void => {
                    setCoordinateType(value as CoordinateType);
                    resource.set('latLongType', value);
                  }}
                >
                  <option value="Point">{localityText('point')}</option>
                  <option value="Line">{localityText('line')}</option>
                  <option value="Rectangle">{localityText('rectangle')}</option>
                </Select>
              </label>
            </th>
            <th scope="col">{localityText('latitude')}</th>
            <th scope="col">{localityText('longitude')}</th>
            <th scope="col">{localityText('parsed')}</th>
          </tr>
        </thead>
        <tbody>
          <CoordinatePoint
            resource={resource}
            label={
              coordinateType === 'Point'
                ? localityText('coordinates')
                : coordinateType === 'Line'
                ? commonText('start')
                : localityText('northWestCorner')
            }
            index={1}
            isReadOnly={mode === 'view'}
            step={step}
          />
          {coordinateType === 'Point' ? undefined : (
            <CoordinatePoint
              resource={resource}
              label={
                coordinateType === 'Line'
                  ? commonText('end')
                  : localityText('southEastCorner')
              }
              index={2}
              isReadOnly={mode === 'view'}
              step={step}
            />
          )}
        </tbody>
      </table>
    </fieldset>
  );
}
