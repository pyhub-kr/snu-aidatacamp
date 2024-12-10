from crispy_forms.layout import Submit


class JustOneClickableSubmit(Submit):
    field_classes = "btn btn-primary cursor-pointer bg-blue-500 hover:bg-blue-700 text-white text-sm font-bold py-2 px-4 rounded float-right"

    def __init__(self, *, name="submit", value="저장하기", **kwargs):
        onclick = f"""
            this.disabled=true;
            this.value = "처리 중 ...";
            this.form.requestSubmit();
        """
        onclick = "".join(map(lambda s: s.strip(), onclick.splitlines()))
        super().__init__(name, value, onclick=onclick, **kwargs)
