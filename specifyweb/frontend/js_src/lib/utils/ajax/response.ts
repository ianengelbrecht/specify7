import { parseXml } from '../../components/AppResources/codeMirrorLinters';
import { formatConjunction } from '../../components/Atoms/Internationalization';
import { handleAjaxError } from '../../components/Errors/FormatError';
import { f } from '../functools';
import type { RA } from '../types';
import { filterArray } from '../types';
import { sortFunction } from '../utils';
import { Http, httpCodeToErrorMessage } from './definitions';
import type { AjaxErrorMode, AjaxResponseObject, MimeType } from './index';

/**
 * Handle network response (parse the data, handle possible errors)
 */
export function handleAjaxResponse<RESPONSE_TYPE = string>({
  expectedErrors,
  accept,
  response,
  errorMode,
  text,
}: {
  readonly expectedErrors: RA<number>;
  readonly accept: MimeType | undefined;
  readonly response: Response;
  readonly errorMode: AjaxErrorMode;
  readonly text: string;
}): AjaxResponseObject<RESPONSE_TYPE> {
  // BUG: silence all errors if the page begun reloading
  try {
    if (response.ok || expectedErrors.includes(response.status)) {
      if (response.ok && accept === 'application/json') {
        try {
          return { data: JSON.parse(text), response, status: response.status };
        } catch {
          throw {
            type: 'jsonParseFailure',
            statusText: 'Failed parsing JSON response:',
            responseText: text,
          };
        }
      } else if (response.ok && accept === 'text/xml') {
        const parsed = parseXml(text);
        if (typeof parsed === 'object')
          return {
            // Assuming that RESPONSE_TYPE extends Document
            data: parsed as unknown as RESPONSE_TYPE,
            response,
            status: response.status,
          };
        else
          throw {
            type: 'xmlParseFailure',
            statusText: `Failed parsing XML response: ${parsed}`,
            responseText: text,
          };
      } else
        return {
          // Assuming that RESPONSE_TYPE extends string
          data: text as unknown as RESPONSE_TYPE,
          response,
          status: response.status,
        };
    } else if (response.status === Http.FORBIDDEN)
      throw {
        type: 'permissionDenied',
        statusText: "You don't have a permission to do this action",
        responseText: text,
      };
    else {
      throw {
        type: 'invalidResponseCode',
        statusText: filterArray([
          `Invalid response code ${response.status}. ${
            expectedErrors.length > 0
              ? `Expected ${
                  expectedErrors.length === 1 ? '' : 'one of '
                }${formatConjunction(
                  Array.from(expectedErrors)
                    .sort(sortFunction(f.id))
                    .map(f.toString)
                )}.`
              : ''
          }`,
          httpCodeToErrorMessage[response.status],
          'Response:',
        ]),
        responseText: text,
      };
    }
  } catch (error) {
    console.error(error);
    handleAjaxError(error, response, errorMode);
  }
}
