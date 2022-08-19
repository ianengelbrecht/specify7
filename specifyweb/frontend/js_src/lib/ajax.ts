import { parseXml } from './codemirrorlinters';
import { handleAjaxError } from './components/errorboundary';
import { formatList } from './components/internationalization';
import { csrfToken } from './csrftoken';
import { f } from './functools';
import { sortFunction } from './helpers';
import type { IR, PartialBy, RA } from './types';

export const isExternalUrl = (url: string): boolean =>
  /*
   * Blob URLs may point to the same origin, but should be treated as external
   * by the navigator
   */
  url.startsWith('blob:') ||
  new URL(url, globalThis.location.origin).origin !==
    globalThis.location.origin;

// Make sure the given URL is from current origin and give back the relative path
export function toRelativeUrl(url: string): string | undefined {
  const parsed = new URL(url, globalThis.location.origin);
  return parsed.origin === globalThis.location.origin
    ? `${parsed.pathname}${parsed.search}${parsed.hash}`
    : undefined;
}

// These HTTP methods do not require CSRF protection
export const csrfSafeMethod = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE']);

// REFACTOR: add a central place for all API endpoint definitions

// FEATURE: make all back-end endpoints accept JSON
/**
 * Convert JSON object to FormData.
 * Some endpoints accept form data rather than stringified JSON.
 * Just wrap your JS object in a call to formData() before passing it as a
 * "body" to ajax()
 */
export function formData(
  data: IR<Blob | RA<number | string> | boolean | number | string>
): FormData {
  const formData = new FormData();
  Object.entries(data).forEach(([key, value]) =>
    formData.append(
      key,
      Array.isArray(value)
        ? JSON.stringify(value)
        : typeof value === 'number'
        ? value.toString()
        : typeof value === 'boolean'
        ? value.toString()
        : value
    )
  );
  return formData;
}

/* An enum of HTTP status codes back-end commonly returns */
export const Http = {
  // You may add others codes as needed
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  NOT_FOUND: 404,
  FORBIDDEN: 403,
  CONFLICT: 409,
  UNAVAILABLE: 503,
} as const;

export type MimeType = 'application/json' | 'application/xml' | 'text/plain';

export type AjaxResponseObject<RESPONSE_TYPE> = {
  /*
   * Parsed response (parser is selected based on the value of options.headers.Accept:
   *   - application/json - json
   *   - application/xml - xml
   *   - else - string
   */
  readonly data: RESPONSE_TYPE;
  readonly response: Response;
  // One of expectedResponseCodes
  readonly status: number;
};

/**
 * Wraps native fetch in useful helpers
 * It is intended as a replacement for jQuery's ajax
 *
 * @remarks
 * Automatically adds CSRF token to non GET requests
 * Casts response to correct typescript type
 */
export const ajax = async <RESPONSE_TYPE = string>(
  url: string,
  /** These options are passed directly to fetch() */
  {
    headers: { Accept: accept, ...headers },
    ...options
  }: Omit<RequestInit, 'body' | 'headers'> & {
    /**
     * If object is passed to body, it is stringified and proper HTTP header is set
     * Can wrap request body object in formData() to encode body as form data
     */
    readonly body?: FormData | IR<unknown> | RA<unknown> | string;
    /**
     * Validates and parses response as JSON if 'Accept' header is 'application/json'
     * Validates and parses response as XML if 'Accept' header is 'application/xml'
     */
    readonly headers: IR<string | undefined> & { readonly Accept?: MimeType };
  },
  /** Ajax-specific options that are not passed to fetch() */
  {
    expectedResponseCodes = [Http.OK],
    strict = true,
  }: {
    /**
     * Throw if returned response code is not what expected
     * If you want to manually handle some error, add that error code here
     */
    readonly expectedResponseCodes?: RA<number>;
    /**
     * If strict, spawn a modal error message dialog on crash
     * In either case, error messages are logged to the console
     */
    readonly strict?: boolean;
  } = {}
): Promise<AjaxResponseObject<RESPONSE_TYPE>> =>
  /*
   * When running in a test environment, mock the calls rather than make
   * actual requests
   * FIXME: replace with a mock
   */
  process.env.NODE_ENV === 'test'
    ? import('./tests/ajax').then(async ({ interceptRequest }) =>
        interceptRequest<RESPONSE_TYPE>(url, expectedResponseCodes)
      )
    : fetch(url, {
        ...options,
        body:
          typeof options.body === 'object' &&
          !(options.body instanceof FormData)
            ? JSON.stringify(options.body)
            : options.body,
        headers: {
          ...(typeof options.body === 'object' &&
          !(options.body instanceof FormData)
            ? {
                'Content-Type': 'application/json',
              }
            : {}),
          ...(csrfSafeMethod.has(options.method ?? 'GET') || isExternalUrl(url)
            ? {}
            : { 'X-CSRFToken': csrfToken }),
          ...headers,
          ...(typeof accept === 'string' ? { Accept: accept } : {}),
        },
      })
        .then(async (response) => Promise.all([response, response.text()]))
        .then(([response, text]: readonly [Response, string]) =>
          handleResponse({
            expectedResponseCodes,
            accept,
            strict,
            response,
            text,
          })
        );

export function handleResponse<RESPONSE_TYPE = string>({
  expectedResponseCodes,
  accept,
  response,
  strict,
  text,
}: {
  readonly expectedResponseCodes: RA<number>;
  readonly accept: MimeType | undefined;
  readonly response: Response;
  readonly strict: boolean;
  readonly text: string;
}): AjaxResponseObject<RESPONSE_TYPE> {
  // BUG: silence all errors if the page begun reloading
  try {
    if (expectedResponseCodes.includes(response.status)) {
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
      } else if (response.ok && accept === 'application/xml') {
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
      console.error('Invalid response', text);
      throw {
        type: 'invalidResponseCode',
        statusText: `Invalid response code ${response.status}. Expected ${
          expectedResponseCodes.length === 1 ? '' : 'one of'
        } ${formatList(
          Array.from(expectedResponseCodes)
            .sort(sortFunction(f.id))
            .map(f.toString)
        )}. Response:`,
        responseText: text,
      };
    }
  } catch (error) {
    console.error(error);
    handleAjaxError(error, response, strict);
  }
}

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
