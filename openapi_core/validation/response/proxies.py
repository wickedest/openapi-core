"""OpenAPI spec validator validation proxies module."""
from typing import Any
from typing import Hashable
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple

from openapi_core.exceptions import OpenAPIError
from openapi_core.spec import Spec
from openapi_core.validation.exceptions import ValidatorDetectError
from openapi_core.validation.request.protocols import Request
from openapi_core.validation.response.datatypes import ResponseValidationResult
from openapi_core.validation.response.protocols import Response
from openapi_core.validation.response.validators import BaseResponseValidator


class DetectResponseValidatorProxy:
    def __init__(
        self, choices: Mapping[Tuple[str, str], BaseResponseValidator]
    ):
        self.choices = choices

    def detect(self, spec: Spec) -> BaseResponseValidator:
        for (key, value), validator in self.choices.items():
            if key in spec and spec[key].startswith(value):
                return validator
        raise ValidatorDetectError("Spec schema version not detected")

    def validate(
        self,
        spec: Spec,
        request: Request,
        response: Response,
        base_url: Optional[str] = None,
    ) -> ResponseValidationResult:
        validator = self.detect(spec)
        return validator.validate(spec, request, response, base_url=base_url)

    def is_valid(
        self,
        spec: Spec,
        request: Request,
        response: Response,
        base_url: Optional[str] = None,
    ) -> bool:
        validator = self.detect(spec)
        error = next(
            validator.iter_errors(spec, request, response, base_url=base_url),
            None,
        )
        return error is None

    def iter_errors(
        self,
        spec: Spec,
        request: Request,
        response: Response,
        base_url: Optional[str] = None,
    ) -> Iterator[Exception]:
        validator = self.detect(spec)
        yield from validator.iter_errors(
            spec, request, response, base_url=base_url
        )
