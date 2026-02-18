# OpenAPI Specification

Interactive API documentation for the Bank of Japan Time-Series Statistics API.

[View raw OpenAPI YAML](https://github.com/obichan117/pyboj/blob/main/openapi.yaml){ .md-button }

<div id="swagger-ui"></div>

<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var el = document.getElementById('swagger-ui');
  if (el) {
    SwaggerUIBundle({
      url: window.location.pathname.replace(/openapi-spec\/?$/, '') + 'assets/openapi.yaml',
      dom_id: '#swagger-ui',
      presets: [SwaggerUIBundle.presets.apis],
      deepLinking: true,
      defaultModelsExpandDepth: 2,
      defaultModelExpandDepth: 2,
    });
  }
});
</script>

<style>
/* Remove Swagger UI's default top bar */
.swagger-ui .topbar { display: none; }
/* Better integration with MkDocs Material */
.swagger-ui .wrapper { padding: 0; }
.swagger-ui .info { margin: 20px 0; }
</style>
