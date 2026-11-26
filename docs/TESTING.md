<div dir="rtl" align="right">

# איך עובדים עם Unit Tests ועם GitHub Actions

## מה זה ולמה

**Unit Test** הוא קטע קוד קצר שמריץ פונקציה אחת שלכם ובודק שהתוצאה נכונה. למשל: האם `encrypt("ATTACKATDAWN", "LEMON")` מחזירה `LXFOPVEFRNHR`. כך עובדים בתעשייה: כותבים קוד, מריצים בדיקות, ומתקנים עד שהכול ירוק.

**GitHub Actions** מריץ את אותן בדיקות בדיוק על שרת של GitHub בכל פעם שאתם פותחים או מעדכנים Pull Request. כך גם אתם וגם המורה רואים מיד אם ההגשה עובדת.

## חלק 1: הרצה במחשב שלכם

### התקנה (פעם אחת)

דרוש Python 3.11 ומעלה. מתוך תיקיית המאגר:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

הקובץ `requirements.txt` מכיל את כל הספריות של הקורס: `pytest` לבדיקות, `matplotlib` לגרפים, `jupyterlab` למחברות ו-`cryptography` למפגשים הבאים.

### הרצת הבדיקות

מריצים תמיד מהתיקייה הראשית של המאגר, עם קוד התלמיד שלכם:

```bash
pytest tests/hw3 --student student05
```

### איך קוראים את הפלט

```
tests/hw3/test_hw3.py ....F..............                    

FAILED tests/hw3/test_hw3.py::test_key_longer_than_message
    assert sol.encrypt("HI", "LEMON") == "SM"
    AssertionError: assert 'SX' == 'SM'
```

- נקודה היא בדיקה שעברה, והאות `F` היא בדיקה שנכשלה.
- שם הבדיקה אומר מה נבדק. כאן: מפתח ארוך מההודעה.
- השורה עם `assert` מראה מה הקוד שלכם החזיר (`SX`) ומה היה צריך לחזור (`SM`).
- בשורה האחרונה מופיע הסיכום, למשל `18 passed, 3 failed`. המטרה: `21 passed`.

### פקודות שימושיות

| פקודה | מה היא עושה |
|---|---|
| `pytest tests/hw3 --student student05 -x` | עוצרת בכישלון הראשון |
| `pytest tests/hw3 --student student05 -v` | מציגה את השם של כל בדיקה |
| `pytest tests/hw3 --student student05 -k encrypt` | מריצה רק בדיקות שהשם שלהן מכיל encrypt |
| `pytest tests/hw3 --student student05 --lf` | מריצה רק את מה שנכשל בפעם הקודמת |

**שיטת עבודה מומלצת:** הבדיקות מסודרות מהקל לקשה. הריצו עם `-x`, תקנו את הכישלון הראשון, והריצו שוב.

מותר ורצוי לקרוא את קובץ הבדיקות `tests/hw3/test_hw3.py` כדי להבין מה נדרש. אסור לשנות אותו.

## חלק 2: GitHub Actions

### מה קורה כשמגישים

1. עושים push ל-branch שלכם ופותחים Pull Request אל `main`.
2. GitHub מזהה שהשתנו קבצים בתיקיית `hw3` ומפעיל את הבדיקה `HW3 tests`.
3. אחרי כדקה מופיע בתחתית ה-Pull Request סימן ירוק (עבר) או איקס אדום (נכשל).

### איך רואים מה נכשל

1. בדף ה-Pull Request לוחצים על הלשונית **Checks**, או על **Details** ליד הבדיקה האדומה.
2. פותחים את השלב **Run the unit tests**. הפלט שם זהה למה שרואים במחשב.
3. מתקנים במחשב, מוודאים שהבדיקות עוברות אצלכם, ועושים commit ו-push לאותו branch. הבדיקה רצה שוב לבד, ואין צורך לפתוח Pull Request חדש.

### למה הבדיקה נכשלת עוד לפני שהקוד רץ

השלב **Find the student folder** נכשל בשני מקרים:

- ה-Pull Request משנה קובץ מחוץ לתיקייה `students/studentXX/` שלכם, למשל קובץ בדיקות או README.
- ה-Pull Request משנה תיקיות של יותר מתלמיד אחד.

הפתרון: להחזיר את הקבצים האלה למצב המקורי ולעשות push שוב.

### עבר במחשב ונכשל ב-GitHub?

הסיבות הנפוצות:

- שכחתם לעשות `git add` לקובץ, למשל `answers.md` או הגרף.
- הקוד קורא קובץ בנתיב שקיים רק במחשב שלכם. השתמשו בפונקציה `load_ciphertext` שבתבנית.
- השתמשתם בספרייה שלא מופיעה ב-`requirements.txt`. בקשו מהמורה להוסיף אותה.

## למורה

- **הרצה ידנית לתלמיד אחד:** לשונית Actions, בוחרים `HW3 tests`, לוחצים Run workflow ומקלידים את קוד התלמיד. האפשרות מופיעה רק אחרי שקובץ ה-workflow נמצא ב-`main`.
- **בדיקה במחשב:** אחרי `git fetch` ומעבר ל-branch של התלמיד, מריצים `pytest tests/hw3 --student studentXX -v`.
- **מה הבדיקות לא בודקות:** את איכות התשובות ב-`answers.md` ואת הגרף. הן רק מוודאות שהקבצים קיימים ושיש בהם תוכן. החלק הזה, 60% מהציון, נבדק ידנית.
- **פתרונות:** הקובץ `tests/hw3/expected.json` מכיל רק טביעת SHA-256 של כל הודעה, כך שאי אפשר לשחזר ממנו את התשובה. המפתחות וההודעות נמצאים רק בתיקיית `teacher-only`, שלא עולה למאגר.

</div>
