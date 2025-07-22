from aiogram.fsm.state import State, StatesGroup

class Subject_actions(StatesGroup):
    switch_choose = State()
    switch_edit = State()
    switch_ask = State()
    switch_type = State()
    switch_comments = State()
    edit_SubjectContent_Count = State()
    edit_SubjectName = State()
    edit_SubjectContent = State()
    edit_SubjectComment = State()
    edit_SubjectGroup = State()
    ask_SubjectName = State()

