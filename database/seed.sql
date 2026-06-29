INSERT INTO Admins (name, email, password_hash) VALUES
('Administrator', 'admin@kvcet.edu', 'demo-admin123')
ON DUPLICATE KEY UPDATE email=email;

INSERT INTO Departments (name, short_name, description, level) VALUES
('Computer Science and Engineering', 'CSE', 'Computer science, programming, software engineering and computing fundamentals.', 'UG'),
('Artificial Intelligence and Data Science', 'AI & DS', 'Artificial intelligence, data science, machine learning and analytics.', 'UG'),
('Biomedical Engineering', 'BME', 'Engineering principles for healthcare and biomedical systems.', 'UG'),
('Biotechnology', 'BT', 'Biotechnology and life science applications.', 'Both'),
('Civil Engineering', 'Civil', 'Construction, structural engineering and infrastructure.', 'UG'),
('Electronics and Communication Engineering', 'ECE', 'Electronics, communication systems and embedded technologies.', 'UG'),
('Electrical and Electronics Engineering', 'EEE', 'Electrical systems, power and electronics.', 'UG'),
('Mechanical Engineering', 'MECH', 'Mechanical systems, manufacturing and design.', 'UG'),
('Robotics and Automation', 'RA', 'Robotics, automation and intelligent systems.', 'UG'),
('Automobile Engineering', 'AUTO', 'Automotive systems and vehicle engineering.', 'UG'),
('Master of Business Administration', 'MBA', 'Management and business administration.', 'PG'),
('Master of Computer Applications', 'MCA', 'Computer applications and software development.', 'PG');

INSERT INTO Courses (name, degree, duration, eligibility, description) VALUES
('Computer Science and Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate engineering course in computer science.'),
('Artificial Intelligence and Data Science', 'B.Tech', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate course in AI and data science.'),
('Biomedical Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Engineering course for biomedical applications.'),
('Biotechnology', 'B.Tech', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate biotechnology course.'),
('Civil Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate civil engineering course.'),
('Electronics and Communication Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate ECE course.'),
('Electrical and Electronics Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate EEE course.'),
('Mechanical Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate mechanical engineering course.'),
('Robotics and Automation', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate robotics and automation course.'),
('Automobile Engineering', 'B.E.', '4 Years', 'Pass in 10+2 with Physics, Chemistry and Mathematics as mandatory subjects.', 'Undergraduate automobile engineering course.'),
('Master of Business Administration', 'MBA', '2 Years', 'Bachelor degree from a recognized university.', 'Postgraduate management course.'),
('Master of Computer Applications', 'MCA', '2 Years', 'Bachelor degree with required eligibility as per university regulations.', 'Postgraduate computer applications course.'),
('M.E. Big Data Analytics', 'M.E.', '2 Years', 'Relevant bachelor degree as per university norms.', 'Postgraduate big data analytics course.'),
('M.E. Biometrics and Cyber Security', 'M.E.', '2 Years', 'Relevant bachelor degree as per university norms.', 'Postgraduate biometrics and cyber security course.'),
('M.E. Computer Science Engineering (Networking)', 'M.E.', '2 Years', 'Relevant bachelor degree as per university norms.', 'Postgraduate computer networking course.'),
('M.E. Manufacturing Engineering', 'M.E.', '2 Years', 'Relevant bachelor degree as per university norms.', 'Postgraduate manufacturing engineering course.'),
('M.Tech Biotechnology', 'M.Tech', '2 Years', 'Relevant bachelor degree as per university norms.', 'Postgraduate biotechnology course.');

INSERT INTO FeeStructure (course_id, category, amount, notes) VALUES
(NULL, 'Government Counselling / Management Quota', 'As per Anna University / Government of Tamil Nadu norms', 'Exact fee depends on the admission category. Contact admission office for latest fee structure.');

INSERT INTO Admissions (title, process_steps, eligibility, required_documents, important_dates) VALUES
('Admission Process', 'Apply through Tamil Nadu Engineering Counselling (TNEA) or Management Quota. Fill out the admission application. Submit required documents. Verify eligibility. Pay admission fees. Confirm admission.', 'B.E./B.Tech: Pass in 10+2 with Physics, Chemistry and Mathematics. MCA: Bachelor degree as per university regulations. MBA: Bachelor degree from a recognized university.', '10th mark sheet, 12th mark sheet, transfer certificate, community certificate if applicable, passport size photos, entrance/counselling documents if applicable.', 'TNEA counselling schedule, application opening date, admission last date and commencement of classes change every academic year. Contact admission office for latest dates.');

INSERT INTO Placements (title, details, companies, training_support) VALUES
('Placement Cell', 'Placement Cell provides campus recruitment, aptitude training, soft skills training, mock interviews, resume preparation, group discussion training, higher education guidance, GATE, GRE, TOEFL, CAT and UPSC coaching support, industrial visits and internship support.', 'Company list is updated every placement season by the placement office.', 'Aptitude, soft skills, mock interviews, resume preparation, group discussion and internship support.');

INSERT INTO Hostels (title, facilities, transport_details) VALUES
('Hostel and Transport', 'Separate hostels for boys and girls, Wi-Fi, dining hall, study rooms, security, 24x7 water and electricity.', 'College buses operate across many routes in and around Chennai and Chengalpattu. Contact admission office for available bus routes.');

INSERT INTO Scholarships (name, eligibility, details) VALUES
('Government Scholarships', 'As per government rules.', 'Students may be eligible based on applicable government norms.'),
('Merit Scholarships', 'Based on merit.', 'Scholarships are offered based on eligibility and applicable rules.'),
('Fee Concession for School Toppers', 'School topper eligibility rules apply.', 'Fee concession may be available for eligible school toppers.'),
('Sports Scholarship', 'Based on sports achievement and rules.', 'Sports scholarship may be offered based on eligibility.'),
('Educational Loan Assistance', 'As per bank and college support process.', 'College supports eligible students with educational loan guidance.');

INSERT INTO Contacts (college_name, address, phone, email, website) VALUES
('Karpaga Vinayaga College of Engineering and Technology', 'GST Road, Chinna Kolambakkam, Palayanoor (PO), Chengalpattu District - 603308, Tamil Nadu', '+91 9842069933', 'admission.kvcet@kveg.in', 'https://kveg.in');

INSERT INTO Faculty (name, designation, qualification, specialization) VALUES
('Faculty information can be updated by admin', 'Department Faculty', 'As per college records', 'Department specialization');

INSERT INTO FAQs (question, answer, category) VALUES
('What courses are available?', 'The college offers UG courses such as CSE, AI & DS, Biomedical, Biotechnology, Civil, ECE, EEE, Mechanical, Robotics & Automation and Automobile Engineering. PG courses include MBA, MCA, M.E. Big Data Analytics, M.E. Biometrics & Cyber Security, M.E. CSE Networking, M.E. Manufacturing Engineering and M.Tech Biotechnology.', 'courses'),
('What is the fee structure?', 'Tuition fees are fixed according to Anna University / Government of Tamil Nadu norms. The exact fee depends on Government Counselling or Management Quota.', 'fees'),
('Is hostel available?', 'Separate hostels are available for boys and girls with Wi-Fi, dining hall, study rooms, security and 24x7 water and electricity.', 'hostel');
