import initialState from "./initialState"
import apiClient from "../services/apiClient"

export const REQUEST_DATA = "@@mci/REQUEST_DATA"
export const REQUEST_DATA_SUCCESS = "@@mci/REQUEST_DATA_SUCCESS"
export const REQUEST_DATA_FAILURE = "@@mci/REQUEST_DATA_FAILURE"
export const FETCH_DATA_BY_ID = "@@mci/FETCH_DATA_BY_ID"
export const FETCH_DATA_BY_ID_SUCCESS = "@@mci/FETCH_DATA_BY_ID_SUCCESS"
export const FETCH_DATA_BY_ID_FAILURE = "@@mci/FETCH_DATA_BY_ID_FAILURE"

export default function mciReducer(state = initialState.mci, action={}) {
    switch (action.type) {
        case REQUEST_DATA:
            return{
                ...state,
                isLoading: true,
            }
        case REQUEST_DATA_SUCCESS:
            return{
                ...state,
                isLoading: false,
                error: null,
                data: {
                    ...state.data,
                    [action.data.id]: action.data
                }
            }
        case REQUEST_DATA_FAILURE:
            return{
                ...state,
                isLoading: false,
                error: action.error
            }
        case FETCH_DATA_BY_ID:
            return{
                ...state,
                isLoading: true
            }
        case FETCH_DATA_BY_ID_SUCCESS:
            return{
                ...state,
                isLoading: false,
                error: null,
                data: action.data
            }
        case FETCH_DATA_BY_ID_FAILURE:
            return{
                ...state,
                isLoading: false,
                error: action.error
            }
        default:
            return state
    }
}

export const Actions = {}

Actions.requestData = ({ startValue, endValue, indicator, year, startDate, endDate, location_name, location_type, river_catchment, landcover_type }) => {
    return apiClient({
        url: `/mci/`,
        method: `POST`,
        types: {
            REQUEST: REQUEST_DATA,
            SUCCESS: REQUEST_DATA_SUCCESS,
            FAILURE: REQUEST_DATA_FAILURE,
        },
        options: {
            data: { startValue, endValue, indicator, year, startDate, endDate, location_name, location_type, river_catchment, landcover_type },
            params: {},
        }
    })
}

Actions.retrieveData = ({ download_id }) => {
    return apiClient({
        url: `/mci/download/${download_id}`,
        method: `GETFILE`,
        types: {
            REQUEST: FETCH_DATA_BY_ID,
            SUCCESS: FETCH_DATA_BY_ID_SUCCESS,
            FAILURE: FETCH_DATA_BY_ID_FAILURE
        },
        options: {
            data: {},
            params: {}
        }
    })
}