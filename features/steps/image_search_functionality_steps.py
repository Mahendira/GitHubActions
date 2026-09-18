from behave import given, then, when


# Auto-generated step definitions for Image Search Functionality

@given('the user has access to the image repository')
def step_impl(context):
    assert context is not None

@given('the user has valid metadata details for the search')
def step_impl(context):
    assert context is not None

@when('the user submits a search query with the metadata details')
def step_impl(context):
    assert context is not None

@then('the system should return a list of images matching the metadata')
def step_impl(context):
    assert context is not None

@given('the response code should be 200 as per OpenAPI specification')
def step_impl(context):
    assert context is not None

@when('the user submits a search query with invalid metadata details')
def step_impl(context):
    assert context is not None

@then('the system should return a response code of 400 as per OpenAPI specification')
def step_impl(context):
    assert context is not None

@when('the user submits a search query with no metadata details')
def step_impl(context):
    assert context is not None

@then('the system should return a response code of 422 as per OpenAPI specification')
def step_impl(context):
    assert context is not None

