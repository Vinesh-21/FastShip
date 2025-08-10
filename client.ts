/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** UserType */
export enum UserType {
  Seller = "seller",
  Partner = "partner",
}

/** ShipmentStatus */
export enum ShipmentStatus {
  Placed = "placed",
  InTransit = "in_transit",
  OutForDelivery = "out_for_delivery",
  Delivered = "delivered",
  Cancelled = "cancelled",
}

/** Body_loginDeliveryPartner */
export interface BodyLoginDeliveryPartner {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_loginSeller */
export interface BodyLoginSeller {
  /** Grant Type */
  grant_type?: string | null;
  /** Username */
  username: string;
  /**
   * Password
   * @format password
   */
  password: string;
  /**
   * Scope
   * @default ""
   */
  scope?: string;
  /** Client Id */
  client_id?: string | null;
  /**
   * Client Secret
   * @format password
   */
  client_secret?: string | null;
}

/** Body_reset_password */
export interface BodyResetPassword {
  /** Password */
  password: string;
}

/** DeliveryPartnerCreate */
export interface DeliveryPartnerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /** Password */
  password: string;
}

/** DeliveryPartnerRead */
export interface DeliveryPartnerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
}

/** DeliveryPartnerResponse */
export interface DeliveryPartnerResponse {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
  /**
   * Id
   * @format uuid
   */
  id: string;
}

/** DeliveryPartnerUpdate */
export interface DeliveryPartnerUpdate {
  /** Serviceable Zip Codes */
  serviceable_zip_codes: number[];
  /** Max Handling Capacity */
  max_handling_capacity: number;
}

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** SellerCreate */
export interface SellerCreate {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /** Password */
  password: string;
  /** Zip Code */
  zip_code: number;
}

/** SellerRead */
export interface SellerRead {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
}

/** SellerResponse */
export interface SellerResponse {
  /** Name */
  name: string;
  /**
   * Email
   * @format email
   */
  email: string;
  /**
   * Id
   * @format uuid
   */
  id: string;
}

/** ShipmentCreate */
export interface ShipmentCreate {
  /** Content */
  content: string;
  /**
   * Weight
   * @max 25
   */
  weight: number;
  /** Destination */
  destination: number;
  /**
   * Client Contact Email
   * @format email
   */
  client_contact_email: string;
  /** Client Contact Phone */
  client_contact_phone?: string | null;
}

/** ShipmentEvent */
export interface ShipmentEvent {
  /**
   * Id
   * @format uuid
   */
  id: string;
  /**
   * Created At
   * @format date-time
   */
  created_at: string;
  /** Location */
  location: number;
  status: ShipmentStatus;
  /** Description */
  description?: string | null;
  /**
   * Shipment Id
   * @format uuid
   */
  shipment_id: string;
}

/** ShipmentRead */
export interface ShipmentRead {
  /** Content */
  content: string;
  /**
   * Weight
   * @max 25
   */
  weight: number;
  /** Destination */
  destination: number;
  /**
   * Id
   * @format uuid
   */
  id: string;
  /** Timeline */
  timeline: ShipmentEvent[];
  /**
   * Estimated Delivery
   * @format date-time
   */
  estimated_delivery: string;
}

/** ShipmentUpdate */
export interface ShipmentUpdate {
  /** Location */
  location?: number | null;
  /** Description */
  description?: string | null;
  /** Verification Otp */
  verification_otp?: number | null;
  status?: ShipmentStatus | null;
  /** Estimated Delivery */
  estimated_delivery?: string | null;
}

/** TokenData */
export interface TokenData {
  /** Access Token */
  access_token: string;
  /** Type */
  type: string;
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

import type {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  HeadersDefaults,
  ResponseType,
} from "axios";
import axios from "axios";

export type QueryParamsType = Record<string | number, any>;

export interface FullRequestParams
  extends Omit<AxiosRequestConfig, "data" | "params" | "url" | "responseType"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseType;
  /** request body */
  body?: unknown;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown>
  extends Omit<AxiosRequestConfig, "data" | "cancelToken"> {
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<AxiosRequestConfig | void> | AxiosRequestConfig | void;
  secure?: boolean;
  format?: ResponseType;
}

export enum ContentType {
  Json = "application/json",
  JsonApi = "application/vnd.api+json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public instance: AxiosInstance;
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private secure?: boolean;
  private format?: ResponseType;

  constructor({
    securityWorker,
    secure,
    format,
    ...axiosConfig
  }: ApiConfig<SecurityDataType> = {}) {
    this.instance = axios.create({
      ...axiosConfig,
      baseURL: axiosConfig.baseURL || "",
    });
    this.secure = secure;
    this.format = format;
    this.securityWorker = securityWorker;
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected mergeRequestParams(
    params1: AxiosRequestConfig,
    params2?: AxiosRequestConfig,
  ): AxiosRequestConfig {
    const method = params1.method || (params2 && params2.method);

    return {
      ...this.instance.defaults,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...((method &&
          this.instance.defaults.headers[
            method.toLowerCase() as keyof HeadersDefaults
          ]) ||
          {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected stringifyFormItem(formItem: unknown) {
    if (typeof formItem === "object" && formItem !== null) {
      return JSON.stringify(formItem);
    } else {
      return `${formItem}`;
    }
  }

  protected createFormData(input: Record<string, unknown>): FormData {
    if (input instanceof FormData) {
      return input;
    }
    return Object.keys(input || {}).reduce((formData, key) => {
      const property = input[key];
      const propertyContent: any[] =
        property instanceof Array ? property : [property];

      for (const formItem of propertyContent) {
        const isFileType = formItem instanceof Blob || formItem instanceof File;
        formData.append(
          key,
          isFileType ? formItem : this.stringifyFormItem(formItem),
        );
      }

      return formData;
    }, new FormData());
  }

  public request = async <T = any, _E = any>({
    secure,
    path,
    type,
    query,
    format,
    body,
    ...params
  }: FullRequestParams): Promise<AxiosResponse<T>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const responseFormat = format || this.format || undefined;

    if (
      type === ContentType.FormData &&
      body &&
      body !== null &&
      typeof body === "object"
    ) {
      body = this.createFormData(body as Record<string, unknown>);
    }

    if (
      type === ContentType.Text &&
      body &&
      body !== null &&
      typeof body !== "string"
    ) {
      body = JSON.stringify(body);
    }

    return this.instance.request({
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type ? { "Content-Type": type } : {}),
      },
      params: query,
      responseType: responseFormat,
      data: body,
      url: path,
    });
  };
}

/**
 * @title FastShip
 * @version 0.1.0
 * @contact FastShip Support <support@fastship.com> (https://fastship.com/contact)
 *
 *
 * Delivery Managment System For Sellers And Delivery Partners
 *
 * ### Sellers
 * - Can Submit Shipments effortlessly
 *
 * ### Delivery Partners
 * - Auto Accept Shipments
 * - Track and Update Shipment Status
 * - On Status Updates Sends Mail and SMS To The Clients
 *
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  seller = {
    /**
     * No description
     *
     * @tags Seller
     * @name SignupSeller
     * @summary Signupseller
     * @request POST:/seller/signup
     */
    signupSeller: (data: SellerCreate, params: RequestParams = {}) =>
      this.request<SellerRead, HTTPValidationError>({
        path: `/seller/signup`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LoginSeller
     * @summary Loginseller
     * @request POST:/seller/token
     */
    loginSeller: (data: BodyLoginSeller, params: RequestParams = {}) =>
      this.request<TokenData, HTTPValidationError>({
        path: `/seller/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name GetSellerProfile
     * @summary Getsellerprofile
     * @request GET:/seller/seller/me
     * @secure
     */
    getSellerProfile: (params: RequestParams = {}) =>
      this.request<SellerResponse, any>({
        path: `/seller/seller/me`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name LogoutSeller
     * @summary Logoutseller
     * @request GET:/seller/logout
     * @secure
     */
    logoutSeller: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/seller/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ForgotPassword
     * @summary Forgotpassword
     * @request GET:/seller/forgot_password
     */
    forgotPassword: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/forgot_password`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Seller
     * @name ResetPassword
     * @summary Reset Password
     * @request POST:/seller/reset_password
     */
    resetPassword: (
      query: {
        /** Token */
        token: string;
      },
      data: BodyResetPassword,
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/seller/reset_password`,
        method: "POST",
        query: query,
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),
  };
  shipment = {
    /**
     * No description
     *
     * @tags Shipment
     * @name GetShipment
     * @summary Getshipment
     * @request GET:/shipment/
     */
    getShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * @description Create A New Shipment
     *
     * @tags Shipment
     * @name CreateShipment
     * @summary Createshipment
     * @request POST:/shipment/
     * @secure
     */
    createShipment: (data: ShipmentCreate, params: RequestParams = {}) =>
      this.request<ShipmentRead, void | HTTPValidationError>({
        path: `/shipment/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name UpdateShipment
     * @summary Updateshipment
     * @request PATCH:/shipment/
     * @secure
     */
    updateShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      data: ShipmentUpdate,
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/`,
        method: "PATCH",
        query: query,
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name GetAllShipments
     * @summary Getallshipments
     * @request GET:/shipment/allShipments
     */
    getAllShipments: (
      query: {
        user_type: UserType;
        /**
         * User Id
         * @format uuid
         */
        user_id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead[], HTTPValidationError>({
        path: `/shipment/allShipments`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Shipment
     * @name CancelShipment
     * @summary Cancelshipment
     * @request GET:/shipment/cancel
     * @secure
     */
    cancelShipment: (
      query: {
        /**
         * Id
         * @format uuid
         */
        id: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<ShipmentRead, HTTPValidationError>({
        path: `/shipment/cancel`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),
  };
  partner = {
    /**
     * No description
     *
     * @tags Delivery Partner
     * @name SignupDeliveryPartner
     * @summary Signupdeliverypartner
     * @request POST:/partner/signup
     */
    signupDeliveryPartner: (
      data: DeliveryPartnerCreate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/signup`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LoginDeliveryPartner
     * @summary Logindeliverypartner
     * @request POST:/partner/token
     */
    loginDeliveryPartner: (
      data: BodyLoginDeliveryPartner,
      params: RequestParams = {},
    ) =>
      this.request<TokenData, HTTPValidationError>({
        path: `/partner/token`,
        method: "POST",
        body: data,
        type: ContentType.UrlEncoded,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name GetDeliveryPartnerProfile
     * @summary Getdeliverypartnerprofile
     * @request GET:/partner/partner/me
     * @secure
     */
    getDeliveryPartnerProfile: (params: RequestParams = {}) =>
      this.request<DeliveryPartnerResponse, any>({
        path: `/partner/partner/me`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name UpdateDeliveryPartner
     * @summary Updatedeliverypartner
     * @request POST:/partner/
     * @secure
     */
    updateDeliveryPartner: (
      data: DeliveryPartnerUpdate,
      params: RequestParams = {},
    ) =>
      this.request<DeliveryPartnerRead, HTTPValidationError>({
        path: `/partner/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name LogoutDeliveryPartner
     * @summary Logoutdeliverypartner
     * @request GET:/partner/logout
     * @secure
     */
    logoutDeliveryPartner: (params: RequestParams = {}) =>
      this.request<any, any>({
        path: `/partner/logout`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Delivery Partner
     * @name ForgotPasswordPartner
     * @summary Forgotpasswordpartner
     * @request GET:/partner/forgot_password
     */
    forgotPasswordPartner: (
      query: {
        /**
         * Email
         * @format email
         */
        email: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<any, HTTPValidationError>({
        path: `/partner/forgot_password`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),
  };
}
