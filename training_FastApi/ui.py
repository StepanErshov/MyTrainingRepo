import streamlit as st
import requests

st.set_page_config(layout="wide")

def hide_streamlit_conf():
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)

    hide_streamlit_style = """
                    <style>
                    div[data-testid="stToolbar"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stDecoration"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stStatusWidget"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    #MainMenu {
                    visibility: hidden;
                    height: 0%;
                    }
                    header {
                    visibility: hidden;
                    height: 0%;
                    }
                    footer {
                    visibility: hidden;
                    height: 0%;
                    }
                    </style>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

BASE_URL = "http://localhost:8000"

def get_all_books():
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 202:
        return response.json()
    return []

def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    if response.status_code == 200:
        return response.json()
    return None

def create_book(book_data):
    response = requests.post(f"{BASE_URL}/books/", json=book_data)
    return response.status_code == 201

def update_book(book_id, book_data):
    response = requests.put(
        f"{BASE_URL}/books/{book_id}",
        json=book_data,
        headers={"Content-Type": "application/json"}
    )
    return response.status_code == 200

def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    return response.status_code == 204

def main():
    st.title("Управление книгами")
    
    menu = ["Просмотр книг", "Добавить книгу", "Обновить книгу", "Удалить книгу"]
    choice = st.sidebar.selectbox("Меню", menu)
    
    if choice == "Просмотр книг":
        st.subheader("Список книг")
        books = get_all_books()
        if books:
            for book in books:
                st.write(f"ID: {book['id']}")
                st.write(f"Название: {book['title']}")
                st.write(f"Автор: {book['author']}")
                st.write("---")
        else:
            st.warning("Книги не найдены")
            
    elif choice == "Добавить книгу":
        st.subheader("Добавить новую книгу")
        with st.form(key="add_book_form"):
            id = st.number_input("ID", min_value=1, step=1)
            title = st.text_input("Название")
            author = st.text_input("Автор")
            submit_button = st.form_submit_button("Добавить")
            
            if submit_button:
                book_data = {
                    "id": id,
                    "title": title,
                    "author": author
                }
                if create_book(book_data):
                    st.success("Книга успешно добавлена!")
                else:
                    st.error("Ошибка при добавлении книги")
    
    elif choice == "Обновить книгу":
        st.subheader("Обновить информацию о книге")
        book_id = st.number_input("Введите ID книги", min_value=1, step=1)
        
        if 'book_found' not in st.session_state:
            st.session_state.book_found = False
        
        if st.button("Найти книгу"):
            book = get_book(book_id)
            if book:
                st.session_state.current_book = book
                st.session_state.book_found = True
            else:
                st.warning("Книга не найдена")
                st.session_state.book_found = False
        
        if st.session_state.get('book_found', False):
            with st.form(key="update_form"):
                book = st.session_state.current_book
                new_title = st.text_input("Название", value=book["title"])
                new_author = st.text_input("Автор", value=book["author"])
                
                if st.form_submit_button("Обновить"):
                    updated_data = {
                        "id": book_id,
                        "title": new_title,
                        "author": new_author
                    }
                    if update_book(book_id, updated_data):
                        st.success("Книга обновлена!")
                        st.session_state.book_found = False
                    else:
                        st.error("Ошибка обновления")
    
    elif choice == "Удалить книгу":
        st.subheader("Удалить книгу")
        book_id = st.number_input("Введите ID книги для удаления", min_value=1, step=1)
        
        if st.button("Удалить"):
            if delete_book(book_id):
                st.success("Книга успешно удалена!")
            else:
                st.error("Ошибка при удалении книги или книга не найдена")

if __name__ == "__main__":
    main()