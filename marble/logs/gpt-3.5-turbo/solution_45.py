# Notebook_CollabSketch.py

class Notebook:
    def __init__(self):
        self.pages = []
        self.current_page = None

    def create_page(self):
        new_page = Page()
        self.pages.append(new_page)
        self.current_page = new_page
        return new_page

    def switch_page(self, page_number):
        if page_number < len(self.pages):
            self.current_page = self.pages[page_number]
        else:
            print("Page number out of range.")

    def get_current_page(self):
        return self.current_page

class Page:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def get_elements(self):
        return self.elements

class Element:
    def __init__(self, element_type, color, size):
        self.element_type = element_type
        self.color = color
        self.size = size

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def draw_element(self, element, page):# Implement comment functionality
        page.add_comment(comment)
        # Implement tagging functionality
        page.tag_element(element)    def tag_element(self, element, page):
        page.tag_element(element)        # Implement comment functionality
        page.add_comment(comment)
        # Implement tagging functionality
        pass

        # Implement tagging functionality
        page.tag_element(element)
# Example Usage
notebook = Notebook()
page1 = notebook.create_page()

user1 = User("Alice", "editor")
user2 = User("Bob", "viewer")

element1 = Element("brush", "blue", 2)
user1.draw_element(element1, page1)

elements_on_page1 = page1.get_elements()
for element in elements_on_page1:
    print(f"Element Type: {element.element_type}, Color: {element.color}, Size: {element.size}")

# Additional functionality can be added based on the requirements mentioned in the task description