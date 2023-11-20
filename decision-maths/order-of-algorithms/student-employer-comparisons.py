
import random

N = 3

def print_list(lst: list) -> None:
	print([str(item) for item in lst])





class Student():
	def __init__(self, identifier) -> None:
		self.identifier = identifier
	
	def __str__(self) -> str:
		return f'<Student \'{self.identifier}\'>'


class Employer():
	def __init__(self, identifier) -> None:
		self.identifier = identifier

	def __str__(self) -> str:
		return f'<Employer \'{self.identifier}\'>'


class RatingRelationship():
	def __init__(self, student: Student, employer: Employer, studentsRating: int, employersRating: int) -> None:
		self.student = student
		self.employer = employer
		self.studentsRating = studentsRating
		self.employersRating = employersRating

	def get_total_rating(self) -> int:
		return self.studentsRating + self.employersRating
	
	def __str__(self) -> str:
		return f'<{self.student} ({self.studentsRating}) - {self.get_total_rating()} - {self.employer} ({self.employersRating})>'


students = [Student(i + 1) for i in range(N)]
employers = [Employer(i + 1) for i in range(N)]

print_list(students)

ratingRelationships = []

for student in students:
	
	for employer in employers:
		print('----')
		print(student, employer)
		newRatingsRelation = RatingRelationship(student, employer, random.randint(1, 10), random.randint(1, 10))
		print(newRatingsRelation)
		print('----')
		ratingRelationships.append(newRatingsRelation)

print_list(ratingRelationships)

sortedRatingsList = sorted(ratingRelationships, key=lambda ratingRelation: ratingRelation.get_total_rating())

print()

print_list(ratingRelationships)
print_list(sortedRatingsList)
print('-----')

employmentMatches = []
comparisonCount = 0

while len(sortedRatingsList) > 0:
	newRatingList = []
	highestRatingRelation = sortedRatingsList[-1]

	employmentMatches.append(highestRatingRelation)

	for rating in sortedRatingsList:
		if rating.student != highestRatingRelation.student and rating.employer != highestRatingRelation.employer:
			newRatingList.append(rating)
		
		comparisonCount += 2

	print_list(sortedRatingsList)
	print_list(newRatingList)

	sortedRatingsList = newRatingList

print(f'Total comparisons: {comparisonCount}')
