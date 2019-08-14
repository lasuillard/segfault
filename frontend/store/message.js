import { ADD_ERROR_LOG, DELETE_ERROR_LOG } from './mutation-types'

class ErrorLog {
  constructor(type, status, title, message, error, extra) {
    this.id      = (ErrorLog.autoId++),
    this.type    = type || 'unknown',
    this.status  = status || 500,
    this.title   = title || error.name,
    this.message = message || error.message,
    this.error   = error 
    this.extra   = extra
  }
}
ErrorLog.autoId = 0

/*
  ErrorLog list item format:
  {
    (AUTO)type: string in ['client-request' 'server-response', 'application', 'unknown']
    (AUTO)status: nuermic HTTP Status Code
    (SEMI-AUTO)title: user defined string
    (SEMI-AUTO)message: user defined string
    (AUTO)error: raw error object
    (SEMI-AUTO)extra: additional informations 
  }

  message print format(show as tree):
  ▼ preview:
    ${status} ${title}
    ▼ detail:
      ${title}
      ${message}
      ▼ error:
        ${error}
      ▼ extra:
        ${extra}
*/

export const state = () => ({
  list: []
})

export const getters = {

}

export const mutations = {
  [ADD_ERROR_LOG]: ({ list }, obj) => {
    // put item into list
    list.push(new ErrorLog(...obj))
  },
  [DELETE_ERROR_LOG]: ({ list }, id) => {
    // remove item from list
    var index = list.findIndex((v) => { return v.id == id })
    if (index == -1)
      return

    list.splice(index, 1)
  }
}

export const actions = {
  logAxiosError: (context, axiosError, extraPayload) => {
    /*
      process error object of axios

      @return message
    */
    let { request, response, config } = axiosError
    let type, status, title, message, extra

    title = extraPayload.title || ''
    message = extraPayload.message || ''
    if (response) {
      // The request has been made and server responded with status code(2xx)
      type = 'server-response'
      status = response.status
      extra = {
        headers: response.headers,
        data: response.data,
      }
    } else if (request) {
      // The request was made but no response received
      type = 'unknown'
      status = 'none'

    } else {
      // configuration error
      type = 'application'
      status = 'none'

    }
    extra = {
      ...extra,
      config: config
    }

    context.commit(
      ADD_ERROR_LOG,
      new ErrorLog(type, status, title, message, axiosError, extra)
    )
  }
}
