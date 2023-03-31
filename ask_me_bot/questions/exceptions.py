class DataInsertError(Exception):
    pass


class DataUpdateError(Exception):
    pass


class DataKeysError(Exception):
    pass


class ThemeNotExistedError(Exception):
    pass


class QuestionLengthError(Exception):
    pass


class ExplanationLengthError(Exception):
    pass


class DetailExplanationLengthError(Exception):
    pass


class AnswerLengthError(Exception):
    pass


class LotIncorrectAnswersError(Exception):
    pass


class GetQuestionWithThemeNameError(Exception):
    pass


class GetAnswersForQuestionError(Exception):
    pass


class ExistingThemeError(Exception):
    pass


class JsonIncorrectData(Exception):
    pass
