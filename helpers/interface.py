from collections import OrderedDict


class Interface:
    """
    Generate command line interactive interface menu and handle the interaction with it
    """

    def __init__(self, title="", message="", delimiter="X", width=60, box_weight=1,
                 top_weight=None, left_weight=None, right_weight=None, bottom_weight=None,
                 invalid_option_message="Opção não é válida!", show_out_option=True,
                 out_option_text="Sair", out_option_label="X", padding=1, bottom_padding=None,
                 top_padding=None, left_padding=None, right_padding=None, return_selected_option=False):
        """
        Args:
            title: Title of interface
            message: Message showed when interface is running
            delimiter: Text used to delimit interface's box
            invalid_option_message: Message displayed when an invalid option is selected
            return_selected_option: Boolean. Defines if value of the option selected by user will be returned or called

            show_out_option: Boolean. Define if the out option will be showed in menu
            out_option_text: Text of out menu entry
            out_option_label: Label of the out menu entry

            Layout Parameters
            width: External width of interface in characters

            box_weight: Number of delimiter characters in the border. Can be overridden by top_weight, left_weight,
                        right_weight and bottom_weight args

            padding: Space between border and content. Can be overridden by top_padding, left_padding, right_padding and
                     bottom_padding
        """

        # Data options
        self.title = title
        self.message = message
        self.menu_options = OrderedDict()
        self.delimiter = delimiter
        self.invalid_option_message = invalid_option_message

        # Behavior options
        self.return_selected_option = return_selected_option

        # Out option config parameters
        self.show_out_option = show_out_option
        self.out_option_text = out_option_text
        self.out_option_label = str(out_option_label)

        # Layout options
        self.width = width

        # Padding config parameters
        self.bottom_padding = bottom_padding if bottom_padding is not None else padding
        self.top_padding = top_padding if top_padding is not None else padding
        self.left_padding = left_padding if left_padding is not None else padding
        self.right_padding = right_padding if right_padding is not None else padding

        # Border weight config parameters
        self.top_weight = top_weight if top_weight is not None else box_weight
        self.left_weight = left_weight if left_weight is not None else box_weight
        self.right_weight = right_weight if right_weight is not None else box_weight
        self.bottom_padding = bottom_weight if bottom_weight is not None else box_weight

    def add_menu_option(self, label, callback, *args, **kwargs):
        """
        Add an entry to menu

        Args:
            label: Text label of menu option
            callback: Value that menu option represents. Can be any type of object. If the parameter
                      return_selected_option is settled to False (as default), needs to be a callable
            *args: arguments to pass for callback. Only relevant if the attribute return_selected_option is False
            **kwargs: keyword arguments to pass for callback. Only relevant if the attribute
                      return_selected_option is False

        Returns:
            None
        """
        self.menu_options[label] = {
            "callback": callback,
            "args": args,
            "kwargs": kwargs
        }

    def remove_menu_option(self, label):
        """
        Removes an entry of menu
        Args:
            label: Label of entry to be removed

        Returns:
            None
        """
        del self.menu_options[label]

    def run(self):
        """
        Runs interface and handles selected options until the out option is selected or until an valid option is
        selected if the parameter 'return_selected_option' is True

        Returns:
            The callback of selected menu option or call it
        """

        prompt_message = self._build_prompt_message()
        while True:
            selected_option = input(prompt_message)

            if selected_option == self.out_option_label:
                return None

            try:
                selected_index = int(selected_option) - 1
                selected = list(self.menu_options.items())[selected_index][1]

                callback = selected["callback"]
                args = selected["args"]
                kwargs = selected["kwargs"]

                if self.return_selected_option:
                    return callback
                else:
                    callback(*args, **kwargs)

            except (IndexError, KeyError, ValueError):
                print(self.invalid_option_message)

    def _build_prompt_message(self):
        used_width = ((self.left_weight + self.right_weight) * len(self.delimiter)) + self.right_padding + self.left_padding
        util_width = self.width - used_width
        title_pattern = "{:^%d}" % util_width
        option_pattern = "{:<%d}" % util_width

        prompt_message = ""

        # Delimiting top box delimiter
        for i in range(self.top_weight):
            prompt_message += self.delimiter * (self.width // len(self.delimiter)) + "\n"

        # Adding top padding
        for i in range(self.top_padding):
            prompt_message += self._build_line(title_pattern, "")

        # Adding title and message, if defined
        if self.title:
            prompt_message += self._build_line(title_pattern, self.title)

        if self.message:
            prompt_message += self._build_line(title_pattern, self.message)

        if self.title or self.message:
            prompt_message += self._build_line(title_pattern, "")

        # Adding options in menu
        for n, label in enumerate(self.menu_options):
            option = "{}. {}".format(n + 1, label)
            prompt_message += self._build_line(option_pattern, option)

        # Adding "out" option
        if self.show_out_option:
            out_option = "{}. {}".format(self.out_option_label, self.out_option_text)
            prompt_message += self._build_line(option_pattern, out_option)

        # Adding bottom padding
        for i in range(self.bottom_padding):
            prompt_message += self._build_line(title_pattern, "")

        # Adding bottom box elimiter
        for i in range(self.bottom_padding):
            prompt_message += self.delimiter * (self.width // len(self.delimiter)) + "\n"

        return prompt_message

    def _build_line(self, pattern, filler):
        left_box_delimiter = self.delimiter * self.left_weight
        right_box_delimiter = self.delimiter * self.right_weight
        left_space = " " * self.left_padding
        right_space = " " * self.right_padding

        return left_box_delimiter + left_space + pattern.format(filler) + right_space + right_box_delimiter + "\n"
