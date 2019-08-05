const auth = require('../src/auth')

describe('src.auth.js', () => {
  test('build query properly', () => {
    expect(auth.buildQuery('http://example.com', {})).toBe('http://example.com')
    expect(auth.buildQuery('http://example.com', {
      test: 'jest',
      e2e: '',
      extra: ''
    })).toBe('http://example.com?test=jest&e2e=&extra=')
  })

  test('returns appropriate login page href for provider', () => {
    expect(auth.getLoginPage('unsupported')).toBeUndefined()
    for (var provider of auth.SUPPORTED_OAUTH_PROVIDERS) {
      expect(auth.getLoginPage(provider)).toBeDefined()
    }
  })

  test('covers all supported providers', () => {
    for (var provider of auth.SUPPORTED_OAUTH_PROVIDERS) {
      expect(auth[`${provider.toUpperCase()}_LOGIN_HREF`]).toBeDefined()
    }
  })
})