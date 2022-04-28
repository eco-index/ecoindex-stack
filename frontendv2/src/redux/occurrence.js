import initialState from "./initialState"
import apiClient from "../services/apiClient"

export const REQUEST_DATA = "@@occurrence/REQUEST_DATA"
export const REQUEST_DATA_SUCCESS = "@@occurrence/REQUEST_DATA_SUCCESS"
export const REQUEST_DATA_FAILURE = "@@occurrence/REQUEST_DATA_FAILURE"
export const FETCH_DATA_BY_ID = "@@occurrence/FETCH_DATA_BY_ID"
export const FETCH_DATA_BY_ID_SUCCESS = "@@occurrence/FETCH_DATA_BY_ID_SUCCESS"
export const FETCH_DATA_BY_ID_FAILURE = "@@occurrence/FETCH_DATA_BY_ID_FAILURE"

export default function occurrenceReducer(state = initialState.occurrences, action={}) {
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

Actions.requestData = ({ classification_level, classification_name, year, startDate, endDate, location_name, location_type }) => {
    return apiClient({
        url: `/occurrence/`,
        method: `POST`,
        types: {
            REQUEST: REQUEST_DATA,
            SUCCESS: REQUEST_DATA_SUCCESS,
            FAILURE: REQUEST_DATA_FAILURE,
        },
        options: {
            data: { classification_level, classification_name, year, startDate, endDate, location_name, location_type },
            params: {},
        }
    })
}

Actions.retrieveData = ({ download_id }) => {
    return apiClient({
        url: `/occurrence/download/${download_id}`,
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