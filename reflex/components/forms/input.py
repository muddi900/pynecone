"""An input component."""

from typing import Dict

from reflex.components.component import EVENT_ARG, Component
from reflex.components.forms.debounce import DebounceInput
from reflex.components.libs.chakra import ChakraComponent
from reflex.utils import imports
from reflex.vars import ImportVar, Var


class Input(ChakraComponent):
    """The Input component is a component that is used to get user input in a text field."""

    tag = "Input"

    # State var to bind the input.
    value: Var[str]

    # The default value of the input.
    default_value: Var[str]

    # The placeholder text.
    placeholder: Var[str]

    # The type of input.
    type_: Var[str] = "text"  # type: ignore

    # The border color when the input is invalid.
    error_border_color: Var[str]

    # The border color when the input is focused.
    focus_border_color: Var[str]

    # If true, the form control will be disabled. This has 2 side effects - The FormLabel will have `data-disabled` attribute - The form element (e.g, Input) will be disabled
    is_disabled: Var[bool]

    # If true, the form control will be invalid. This has 2 side effects - The FormLabel and FormErrorIcon will have `data-invalid` set to true - The form element (e.g, Input) will have `aria-invalid` set to true
    is_invalid: Var[bool]

    # If true, the form control will be readonly.
    is_read_only: Var[bool]

    # If true, the form control will be required. This has 2 side effects - The FormLabel will show a required indicator - The form element (e.g, Input) will have `aria-required` set to true
    is_required: Var[bool]

    # "outline" | "filled" | "flushed" | "unstyled"
    variant: Var[str]

    # "lg" | "md" | "sm" | "xs"
    size: Var[str]

    # Time in milliseconds to wait between end of input and triggering on_change
    debounce_timeout: Var[int]

    def _get_imports(self) -> imports.ImportDict:
        return imports.merge_imports(
            super()._get_imports(),
            {"/utils/state": {ImportVar(tag="set_val")}},
        )

    def get_controlled_triggers(self) -> Dict[str, Var]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            "on_change": EVENT_ARG.target.value,
            "on_focus": EVENT_ARG.target.value,
            "on_blur": EVENT_ARG.target.value,
            "on_key_down": EVENT_ARG.key,
            "on_key_up": EVENT_ARG.key,
        }

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create an Input component.

        Args:
            children: The children of the component.
            props: The properties of the component.

        Returns:
            The component.
        """
        if isinstance(props.get("value"), Var) and props.get("on_change"):
            # create a debounced input if the user requests full control to avoid typing jank
            return DebounceInput.create(
                super().create(*children, **props),
                # Currently default to 50ms, which appears to be a good balance
                debounce_timeout=props.get("debounce_timeout", 50),
            )
        return super().create(*children, **props)


class InputGroup(ChakraComponent):
    """The InputGroup component is a component that is used to group a set of inputs."""

    tag = "InputGroup"


class InputLeftAddon(ChakraComponent):
    """The InputLeftAddon component is a component that is used to add an addon to the left of an input."""

    tag = "InputLeftAddon"


class InputRightAddon(ChakraComponent):
    """The InputRightAddon component is a component that is used to add an addon to the right of an input."""

    tag = "InputRightAddon"


class InputLeftElement(ChakraComponent):
    """The InputLeftElement component is a component that is used to add an element to the left of an input."""

    tag = "InputLeftElement"


class InputRightElement(ChakraComponent):
    """The InputRightElement component is a component that is used to add an element to the right of an input."""

    tag = "InputRightElement"
