class Story:

    def __init__(self, name, description, story_number, points, sprint, developer, dependent_stories):
        self.name = name
        self.descripton = description
        self.story_number = story_number
        self.points = points
        self.sprint = sprint
        self.developer = developer
        self.dependent_stories = dependent_stories