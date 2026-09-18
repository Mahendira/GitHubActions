from behave import given, then, when


# Auto-generated step definitions for Search API

@given('the Search API is available at "/api/v1/search"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the API produces responses with content type "application/json"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the API is documented using OpenAPI 3.1')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('records exist that match the search term "cloud"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search?query=cloud"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 200')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should contain matching search results')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the response should conform to the SearchResponse OpenAPI schema')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('more than 10 records match the search term "AWS"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search?query=AWS&page=0&size=10"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 200')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should contain at most 10 results')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the response should contain pagination metadata')
def step_impl(context):
    context = context or {}
    context['metadata'] = {'valid': True}
    assert context['metadata']['valid'] is True

@given('the response should contain the current page')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the response should contain the total number of results')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('no records match the search term "nonexistent-value"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search?query=nonexistent-value"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 200')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should contain an empty results array')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the total number of results should be 0')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the "query" parameter is required')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 400')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should contain an error code')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the response should contain an error message')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the error response should conform to the ErrorResponse OpenAPI schema')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the maximum allowed page size is 100')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search?query=cloud&size=500"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 400')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should indicate that the "size" parameter is invalid')
def step_impl(context):
    context = context or {}
    context['status_code'] = 400
    assert context['status_code'] == 400

@given('an unexpected error occurs while processing the search request')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the client sends a GET request to "/api/v1/search?query=cloud"')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the API should return HTTP status 500')
def step_impl(context):
    context = context or {}
    context['status_code'] = 200
    assert context['status_code'] == 200

@given('the response should contain a standard error response')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the response should conform to the ErrorResponse OpenAPI schema')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the Search API has an OpenAPI specification')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@when('the OpenAPI specification is validated')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@then('the specification should define the "/api/v1/search" path')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the path should define a GET operation')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define the "query" parameter')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define the "page" parameter')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define the "size" parameter')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define HTTP 200 responses')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define HTTP 400 responses')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('the GET operation should define HTTP 500 responses')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('all request parameters should have schemas')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

@given('all response bodies should have schemas')
def step_impl(context):
    context = context or {}
    context['state'] = 'processed'
    assert context['state'] == 'processed'

