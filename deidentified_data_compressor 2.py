# script for DPSI to siphon out crappy data from
# deidentified csv file

# RULES:
# only keep data for people who
# 1. Have a grade
# 2. Who have interacted with the dat (num_events > 10)

# ADD STATISTICS:
# Ratio of days participated to events for each person
# Interaction levels by class
# Percentage of total people that are left after condensing 

import csv

# row indexes
grade_row = 10
num_events_row = 13
days_active_row = 14
course_id_row = 0

total_rows = 0
condensed_rows = 0
total_activity = 0

courses_enrollment = {}
courses_participation = {}

fin = csv.reader(open("person-course-1-17-DI.csv","rU"))
csv_out_file = open("deidentified_data_output.csv","w")
fout = csv.writer(csv_out_file, delimiter = ',', lineterminator='\n')

for row in fin:
    
    # first row (categories)
    if (total_rows == 0) :
        print row
        
        # write to new file
        row.append("events/day")
        fout.writerow(row)
    
        total_rows += 1

    else :                
        total_rows += 1

        # student's grade
        grade = row[grade_row]
        if grade != '':
            grade = float(grade)        
            
        # number of events
        num_events = row[num_events_row]
        if num_events != '':
            num_events = float(num_events)
            
        # days active
        days_active = row[days_active_row]
        if days_active != '':
            days_active = float(days_active)

        # if they have a grade and have interacted more than 10 times
        if (grade > 0.0) and (num_events > 10.0):
            if (not isinstance(grade, str)) and (not isinstance(num_events, str)):
                condensed_rows += 1
                row.append(float(num_events)/float(days_active))

                # write to new file
                fout.writerow(row)

                ## COURSE ENROLLMENT / Activity ##
                
                # if course hasn't been identified yet
                course_name = row[course_id_row]
                if not (course_name in courses_enrollment):
                    courses_enrollment[course_name] = 1
                    courses_participation[course_name] = int(num_events)

                # if it has --> add to count
                else:
                    courses_enrollment[course_name] += 1
                    courses_participation[course_name] += int(num_events)

                total_activity += int(num_events)
                

percentage = float(condensed_rows) / float(total_rows)
print "Condensed " + str(total_rows) + " down to " + str(condensed_rows) + ": " + '{:.2}'.format(percentage) + "% of original pool"
print "Course enrollment breakdown: "

for key in courses_enrollment:
    
    percentage_enrollment = 100.0 * float(courses_enrollment[key]) / float(condensed_rows)

    if percentage_enrollment < 10.0:
        percentage_enroll_print = '{:.2}'.format(percentage_enrollment)
    else:
        percentage_enroll_print ='{:.3}'.format(percentage_enrollment)

    percentage_activity = 100.0 * float(courses_participation[key]) / float(total_activity)

    if percentage_activity < 10.0:
        percentage_activity_print = '{:.2}'.format(percentage_activity)
    else:
        percentage_activity_print ='{:.3}'.format(percentage_activity)

    print key + ": "
    print "Participation: " + str(courses_enrollment[key]) + " / " + str(condensed_rows) + " = " + percentage_enroll_print + "%"
    print "Activity Events: " + str(courses_participation[key]) + " / " + str(total_activity) + " = " + percentage_activity_print + "%"
    print ""

csv_out_file.close()

