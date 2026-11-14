# Homework 2 – student11

## 1. פענוח ומפתח

הטקסט מכיל 2,019 תווים, מהם 1,664 אותיות ו-355 רווחים. זהו צופן החלפה חד-אלפביתי: כל אות מוצפנת מוחלפת תמיד באותה אות מקורית.

### החלטות פענוח ידניות

- המילה `NIS` חוזרת פעמים רבות ומופיעה בתבניות של מילת יחס/יידוע. ההתאמה `NIS = THE` נתמכת גם במשפטים שמתקבלים לאחר הפענוח.
- `V` היא מילה בת אות אחת, ולכן בדקתי את האפשרות `A`. היא מתאימה למשפט הפותח: `A STRONG WIND PUSHED...`.
- הרצף `NIS KSVAI` הופך ל-`THE BEACH`, ומחזק את ההתאמות של האותיות שכבר זוהו.
- הרצף `VHG CE DP IVQ ICYSQ` הופך ל-`ANY OF US HAD HOPED`. הוא מאמת כמה התאמות נוספות לפי ההקשר.
- לאחר כל התאמה החלפתי את האות בכל הופעה שלה, ובדקתי שהטקסט כולו נשאר אנגלית תקינה ולא רק מילים בודדות.

### מפתח שנמצא

ההתאמות שאפשר לאמת מהטקסט הן:

| אות מוצפנת | אות מקורית |
|---|---|
| A | C |
| B | W |
| C | O |
| D | U |
| E | F |
| G | Y |
| H | N |
| I | H |
| J | I |
| K | B |
| L | G |
| M | M |
| N | T |
| O | R |
| P | S |
| Q | D |
| R | L |
| S | E |
| T | X |
| U | Q |
| V | A |
| W | V |
| X | K |
| Y | P |

שתי אותיות מוצפנות, `F` ו-`Z`, אינן מופיעות כלל בטקסט. האותיות המקוריות שלא מופיעות בטקסט המפוענח הן `J` ו-`Z`. לכן אי אפשר לדעת מתוך ההודעה בלבד אם `F→J, Z→Z` או `F→Z, Z→J`. אלה שתי השלמות אפשריות של אותו מפתח מבחינת הטקסט שסופק. בקוד בחרתי באפשרות הראשונה רק כדי לייצג מפתח בן 26 אותיות; זו אינה מסקנה שאפשר להוכיח מהטקסט.

מפתח מועמד לפי סדר האותיות המוצפנות A–Z, עם ההשלמה השרירותית:
`CWOUFJYNHIBGMTRSDLEXQAVKPZ`

### הטקסט המפוענח

A STRONG WIND PUSHED THE SAILBOAT ACROSS THE LAKE FASTER THAN ANY OF US HAD HOPED VOLUNTEERS CLEANED THE BEACH AND COLLECTED MORE PLASTIC BOTTLES THAN ANYONE HAD EXPECTED RECYCLING ONE ALUMINUM CAN SAVES ENOUGH ENERGY TO RUN A TELEVISION FOR SEVERAL HOURS THE FIRE DEPARTMENT VISITED THE SCHOOL TO TEACH CHILDREN HOW TO LEAVE A BUILDING SAFELY OUR TEACHER BELIEVES THAT THE BEST WAY TO UNDERSTAND AN IDEA IS TO EXPLAIN IT TO A FRIEND MOST OF THE WATER ON OUR PLANET IS SALTY AND ONLY A SMALL PART CAN BE USED FOR DRINKING THE FOOTBALL TEAM PRACTICED IN THE RAIN UNTIL THE COACH FINALLY SENT EVERYONE HOME A CAREFUL DRIVER CHECKS THE MIRRORS BEFORE CHANGING LANES EVEN ON AN EMPTY ROAD DOCTORS RECOMMEND DRINKING WATER THROUGHOUT THE DAY ESPECIALLY DURING HOT WEATHER THE MUSEUM OPENED A NEW HALL DEVOTED TO THE HISTORY OF CODES MACHINES AND SECRET MESSAGES SCIENTISTS STUDYING THE DEEP OCEAN HAVE FOUND ANIMALS THAT MAKE THEIR OWN LIGHT IN TOTAL DARKNESS OUR CLASS VISITED A FARM WHERE THE COWS WORE COLLARS THAT SENT THEIR LOCATION TO A PHONE BEES COMMUNICATE THE DIRECTION OF FLOWERS TO EACH OTHER BY PERFORMING A KIND OF DANCE A GOOD PASSWORD IS LONG RANDOM AND NEVER USED ON MORE THAN ONE WEBSITE HONEY NEVER SPOILS BECAUSE BEES REMOVE MOST OF THE WATER BEFORE THEY SEAL THE HONEYCOMB THE FESTIVAL ENDED WITH MUSIC IN THE SQUARE AND LIGHTS HANGING BETWEEN THE TREES THE RIVER FLOODED THE FIELDS EVERY SPRING AND LEFT BEHIND RICH SOIL FOR THE FARMERS A SINGLE CLOUD CAN WEIGH MORE THAN A HUNDRED ELEPHANTS YET IT FLOATS ABOVE US THE OLD MAP SHOWED ROADS THAT NO LONGER EXISTED AND VILLAGES THAT HAD BEEN ABANDONED WHEN THE POWER FAILED THE WHOLE NEIGHBORHOOD GATHERED OUTSIDE TO LOOK AT THE STARS THE TRAIN WAS DELAYED BECAUSE A TREE HAD FALLEN ACROSS THE TRACKS DURING THE STORM THE CASTLE WALLS WERE BUILT SO THICK THAT CANNONS COULD BARELY DAMAGE THEM DURING THE ECLIPSE THE BIRDS STOPPED SINGING AND THE AIR SUDDENLY FELT COLD THE SMALL HARBOR TOWN WOKE SLOWLY AS THE FISHING BOATS RETURNED WITH THE MORNING TIDE

## 2. ניסוי שובר תדירויות בלבד

השובר סופר את האותיות בכל קידומת, ממיין אותן מהנפוצה לנדירה, ומצמיד להן לפי הסדר את:
`ETAOINSHRDLCUMWFGYPBVKXJQZ`.

במקרה של שוויון בתדירות, הקוד ממיין לפי סדר אלפביתי. המדד הוא מספר ההתאמות הנכונות מתוך האותיות המוצפנות שהופיעו באותה קידומת ושיש להן התאמה ידועה. שתי האותיות שלא הופיעו כלל אינן נכללות במכנה, משום שהמפתח שלהן אינו ניתן לאימות מהטקסט.

| אורך הקידומת בתווים | התאמות נכונות |
|---:|---:|
| 100 | 4/21 |
| 250 | 2/23 |
| 500 | 6/23 |
| 1000 | 11/23 |
| 2000 | 13/24 |

הגרף נשמר בקובץ `frequency_graph.png`.

## 3. שלוש האותיות שהיו הקשות ביותר

בין האותיות שהשובר טעה בהן, שלוש האותיות הנדירות ביותר בטקסט היו:

| אות מוצפנת | מספר הופעות | האות המקורית | ניחוש השובר |
|---|---:|---|---|
| U | 1 | Q | J |
| Y | 24 | P | B |
| G | 25 | Y | P |

## 4. שאלות למה

### למה האותיות האלה היו קשות?

האות `U` הופיעה פעם אחת בלבד. האות המקורית שלה היא Q, שמופיעה באנגלית בכ-0.095% מהאותיות, ואילו J מופיעה בכ-0.153%. שתי האותיות נדירות מאוד, ולכן הופעה בודדת אינה מספיקה כדי להבחין ביניהן באופן אמין.

האותיות `Y` ו-`G` מופיעות 24 ו-25 פעמים בלבד. הן מייצגות P ו-Y. לפי טבלת התדירויות, P מופיעה בכ-1.93% ו-Y בכ-1.97% מהטקסט האנגלי — הבדל קטן מאוד. גם B, שהשובר הציע במקום P, קרובה יחסית בשכיחותה (כ-1.49%). לכן שינוי קטן במדגם יכול לשנות את סדר הדירוג ולגרום למיפוי שגוי. טבלת תדירויות היא ממוצע של טקסטים רבים, ולא חוק שמבטיח את הסדר בכל טקסט בודד.

### האם אותיות אקראיות בין המילים עוזרות?

ביצעתי ניסוי שבו הוספתי אות אנגלית אקראית כמילה נפרדת בין כל זוג מילים בטקסט המפוענח, הצפנתי מחדש, והרצתי את אותו שובר. חזרתי על הניסוי 30 פעמים עם זרעים אקראיים קבועים לשחזור.

- ללא אותיות אקראיות: 13/24 התאמות נכונות.
- עם אותיות אקראיות: ממוצע של 11.6/24.
- טווח התוצאות: 6 עד 17 התאמות.

בניסוי הזה הוספת האותיות האקראיות הורידה בממוצע את מספר ההתאמות הנכונות. הסיבה היא שהאותיות שהוכנסו משנות את התפלגות התדירויות ומבלבלות את הדירוג. עם זאת, זו אינה הגנה חזקה בפני עצמה: אפשר לנסות לזהות את האותיות שהוכנסו, ובמיוחד אם הן מופיעות כמילים בנות אות אחת, ואז להסיר אותן ולנתח שוב.

### למה מרחב מפתחות עצום הוא הכרחי אבל לא מספיק?

בצופן החלפה יש `26!` אפשרויות למפתח, מספר עצום שמקשה על מעבר שיטתי על כל המפתחות. אבל גודל מרחב המפתחות לבדו אינו מבטיח ביטחון. הצופן משמר את תדירות האותיות ואת דפוסי המילים, ולכן אפשר לנצל את מבנה השפה בלי לבדוק את כל המפתחות.

התוצאות מדגימות זאת: גם בלי חיפוש של כל המפתחות, שובר התדירויות מצא 13 התאמות נכונות מתוך 24 האותיות שהופיעו בטקסט המלא. ניתוח של מילים חוזרות והקשר הצליח לשחזר את הטקסט כולו. כלומר, מספר המפתחות האפשריים גדול, אבל המבנה הסטטיסטי של האנגלית יוצר חולשה שניתן לנצל.

## הערה מתודולוגית

הניסוי מודד שובר תדירויות פשוט בלבד. הוא אינו שובר אוטומטי מתקדם המשתמש בתבניות מילים או במודל n-grams. כמו כן, שתי אותיות המפתח שלא הופיעו בטקסט אינן ניתנות לשחזור חד-משמעי מהצופן הנתון.

## מקורות לטבלת תדירויות אנגלית

- https://math.oxford.emory.edu/site/math125/englishLetterFreqs/
- https://www.cl.cam.ac.uk/teaching/0708/IntroSec/slides-2up.pdf
