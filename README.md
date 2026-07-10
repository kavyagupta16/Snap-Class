# SnapClass
### AI-Verified Attendance for Classrooms — No Roll Call, No Proxy Check-ins

## 🎯 Problems Solved

### 1. Manual Attendance Wastes Class Time
**Core proposition:** Attendance should be a side effect of a student walking into class, not a 5-minute administrative task the teacher repeats every session.

**Implementation:**
- Teacher opens a session and shares a join code for that class
- Student scans in; identity is verified automatically
- Attendance is written to the class roster with no manual entry

### 2. Digital Check-in Systems Are Trivial to Proxy
**Current limitation:** A join code or QR scan only proves *someone* has the code — not that the enrolled student is the one present. Any classmate can check a friend in.

**Solution approach:**
- Bind the join event to a live face match against the student's enrolled encoding (`dlib` + `face_recognition_models`)
- Layer in a voice-embedding check (`resemblyzer` + `librosa`) as a second identity signal for cases where a face capture is weak or ambiguous

### 3. Manual Roster Management Doesn't Scale
**Risk:** Teachers manually adding every student to every class section is slow and error-prone, especially across multiple sections per semester.

**Solution framework:**
- Class join codes are generated as scannable QR codes (`segno`)
- `auto_enroll_dialog` reads the `join-code` query param on load and auto-enrolls a new student session into the class roster via Supabase — no manual add step

## 💡 Technical Implementation

| Component | Implementation Details |
|---|---|
| Multi-role session routing | `st.session_state['login_type']` drives a `match`/`case` in `app.py` → routes to `teacher_screen()`, `student_screen()`, or `home_screen()` |
| Face-based check-in | `dlib` + `face_recognition_models` encode and match a student's face against their enrolled reference |
| Voice verification layer | `resemblyzer` speaker embeddings over `librosa`-preprocessed audio as a secondary identity signal |
| QR-based class join | `segno` generates a per-class join code; scanning it hits the app with `?join-code=...`, triggering auto-enrollment |
| Backend & auth | Supabase stores users, classes, and attendance records; `bcrypt` hashes credentials |

## 🚧 Challenges & Solutions

### Challenge 1: Face Recognition Reliability in Real Classrooms
**Problem:** Lighting, camera angle, and partial occlusion (masks, glasses glare, students turned away) all degrade face-match confidence in a live classroom, not a controlled dataset.

**Solution:**
- Treat face-match as one signal, not the sole gate — low-confidence matches fall back to the voice layer or a teacher-side manual override
- Encode faces once at enrollment and match against that stored encoding rather than re-training per session

### Challenge 2: Proxy / Spoofed Check-ins
**Problem:** A join code alone can't prove who's physically present.

**Solution:**
- Require the face (and optionally voice) match to succeed *within* the active, time-bound class session tied to that specific join code — a captured face has to match both the enrolled student and a currently-live session, not just any code
- This closes the "share the code with a friend" gap that plain QR-only systems have

### Challenge 3: Handling Biometric Data Responsibly
**Problem:** Face and voice data are sensitive personal data. Storing raw images or audio in the repo, in logs, or in the database directly is a privacy and security liability — and a real risk if this is ever a public repo.

**Solution:**
- Store face/voice **embeddings**, not raw images or audio clips
- Keep any real student media out of version control entirely (`.gitignore` datasets/captures)
- Hash all credentials with `bcrypt`; never store plaintext passwords

## 🛠️ Tech Stack
- **Frontend/App:** Streamlit
- **Face Recognition:** dlib, face_recognition_models
- **Voice Verification:** resemblyzer, librosa
- **Backend:** Supabase
- **Auth:** bcrypt
- **QR Generation:** segno
- **Data Handling:** pandas, numpy

## 🚀 Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📌 Roadmap
- [ ] Confidence-score UI for low-certainty matches instead of silent accept/reject
- [ ] Bulk class/roster import for teachers
- [ ] Attendance analytics dashboard (per-student, per-class trends)
