from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



invite_message = """
1. Add flashcards
2. Practice flashcards
3. Exit\n"""
sub_menu_message = """
1. Add a new flashcard
2. Exit\n"""
practice_menu_message = """press "y" to see the answer:
press "n" to skip:
press "u" to update:\n"""
practice_submenu_message = """press "d" to delete the flashcard:
press "e" to edit the flashcard:\n"""
learning_menu_message = """press "y" if your answer is correct:
press "n" if your answer is wrong:\n"""
possible_variants = [1, 2, 3]

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class FlashCard(Base):

    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer, default=0)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_flashcard():
    try:
        user_choice = input(sub_menu_message)
        if int(user_choice) in possible_variants[:2]:
            if int(user_choice) == 1:
                question = ''
                answer = ''
                while question == '':
                    question = input('Question:\n')
                while answer == '':
                    answer = input('Answer:\n')
                new_data = FlashCard(question=question, answer=answer)
                session.add(new_data)
                session.commit()
                add_flashcard()
            else:
                return
        else:
            print(f'\n{user_choice} is not an option')
            add_flashcard()
    except ValueError:
        print(f'\n{user_choice} is not an option')
        add_flashcard()


def leitner_system(cntx):
    choice = input(learning_menu_message)
    if choice == 'y':
        cntx.box += 1
        if cntx.box == 3:
            session.delete(cntx)
        session.commit()
    elif choice == 'n':
        cntx.box = 0
        session.commit()
    else:
        print(f'\n{choice} is not an option')



def practice_flashcards():
    result_list = session.query(FlashCard).all()
    for i in range(len(result_list)):
        print(f'Question: {result_list[i].question}')
        choice = input(practice_menu_message)
        if choice == 'y':
            print(f'Answer: {result_list[i].answer}')
            leitner_system(result_list[i])
        elif choice == 'n':
            leitner_system(result_list[i])
        elif choice == 'u':
            sub_choice = input(practice_submenu_message)
            if sub_choice == 'd':
                session.delete(result_list[i])
                session.commit()
            elif sub_choice == 'e':
                new_question = ''
                new_answer = ''
                while new_question == '':
                    print(f'current question: {result_list[i].question}')
                    new_question = input('please write a new question:\n')
                while new_answer == '':
                    print(f'current answer: {result_list[i].answer}')
                    new_answer = input('please write a new answer:\n')
                result_list[i].question = new_question
                result_list[i].answer = new_answer
                session.commit()
            else:
                print(f'\n{sub_choice} is not an option')
        else:
            print(f'\n{choice} is not an option')
    return


while True:
    try:
        user_choice = input(invite_message)
        if int(user_choice) in possible_variants:
            if int(user_choice) == 1:
                add_flashcard()
            elif int(user_choice) == 2:
                if len(session.query(FlashCard).all()) > 0:
                    practice_flashcards()
                else:
                    print('There is no flashcard to practice!')
                    session.query(FlashCard).delete()
                    session.commit
            else:
                print('Bye!')
                break
        else:
            print(f'\n{user_choice} is not an option')
    except ValueError:
        print(f'\n{user_choice} is not an option')