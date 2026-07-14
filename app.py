from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

app.secret_key = '1ko591415frud73' 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    regtime = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    info = db.Column(db.String(500), nullable=False)
    skill = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)   


with app.app_context(): 
    db.create_all()

GAME_DATA = {
    "Braziliya": "🧪 Peyvənd",
    "Konqo": "🛡️ Mühafizə kostyumu",
    "Yaponiya": "💊 Antibiotiklər",
    "Misir": "💊 Prazikvantel",
    "Kanada": "🛡️ Mühafizə kostyumu",
    "Avstraliya": "🥾 Qoruyucu çəkmələr",
    "Rusiya": "🧪 Peyvənd",
    "Hindistan": "🦟 Repellent",
    "Madaqaskar": "😷 Respirator FFP3",
    "ABŞ": "😷 Respirator FFP3",
    "Özbəkistan": "🦟 Repellent",
    "Avstriya": "😷 Respirator FFP3",
    "Qrenlandiya": "🕸️ Pavlovski toru",
    "Monqolustan": "🛡️ Mühafizə kostyumu",
    "Sudan": "🦟 Repellent",
    "Peru": "🦟 Repellent",
    "Azərbaycan": "🧤 Cüt əlcək",
    "İslandiya": "🧣 Termo-örtük",
    "Efiopiya": "🔦 UV-sterilizator",
    "Vyetnam": "🔬 Ekspress-test dəsti",
    "Somali": "🧼 Antibakterial sabun",
    "Antarktida": "📡 Fövqəladə radio-mayak"
}

GEAR_LABELS = {
    "vaccine": "🧪 Peyvənd",
    "suit": "🛡️ Mühafizə kostyumu",
    "antibiotics": "💊 Antibiotiklər",
    "praziquantel": "💊 Prazikvantel",
    "boots": "🥾 Qoruyucu çəkmələr",
    "repellent": "🦟 Repellent",
    "respirator": "😷 Respirator FFP3",
    "pavlovsky_net": "🕸️ Pavlovski toru",
    "double_gloves": "🧤 Cüt əlcək",
    "thermal_blanket": "🧣 Termo-örtük",
    "uv_sterilizer": "🔦 UV-sterilizator",
    "blood_test_kit": "🔬 Ekspress-test dəsti",
    "antibacterial_soap": "🧼 Antibakterial sabun",
    "radio_beacon": "📡 Fövqəladə radio-mayak"
}

COUNTRIES_DATA = {
    "brazil": {"name": "Braziliya (Amazoniya)", "population": "213 mln", "medicine": "İnkişaf etməkdə olan", "danger_level": "Yüksək", "diseases": [{"name": "Sarı qızdırma", "type": "Virus", "symptoms": "Qızdırma, sarılıq, əzələ ağrıları.", "info": "Ağcaqanadlar vasitəsilə keçən kəskin virus xəstəliyi. Peyvənd mütləqdir.", "fatality": "20-50%", "item_needed": "vaccine"}]},
    "congo": {"name": "Konqo Demokratik Respublikası", "population": "102 mln", "medicine": "Böhranlı", "danger_level": "Kritik", "diseases": [{"name": "Yuxu xəstəliyi", "type": "Parazitlər", "symptoms": "Yuxu pozğunluğu, qızdırma.", "info": "Çe-çe milçəyi vasitəsilə keçir. MSS-ni zədələyir, müalicəsiz ölümcüldür.", "fatality": "100%", "item_needed": "suit"}]},
    "japan": {"name": "Yaponiya (Kənd regionları)", "population": "123 mln", "medicine": "Qabaqcıl", "danger_level": "Aşağı", "diseases": [{"name": "Yapon ensefaliti", "type": "Virus", "symptoms": "Qızdırma, qıcolmalar, iflic.", "info": "Ağcaqanadlar vasitəsilə keçir. Çox vaxt nevroloji fəsadlar buraxır.", "fatality": "20-30%", "item_needed": "antibiotics"}]},
    "egypt": {"name": "Misir (Nil deltası)", "population": "114 mln", "medicine": "Qənaətbəxş", "danger_level": "Orta", "diseases": [{"name": "Şistosomoz", "type": "Parazitlər", "symptoms": "Allergiya, hematuriya.", "info": "Şirin su ilə təmasda dəri vasitəsilə daxil olan parazit qurdlar.", "fatality": "Aşağı", "item_needed": "praziquantel"}]},
    "canada": {"name": "Kanada (Meşə massivləri)", "population": "39 mln", "medicine": "Yüksək", "danger_level": "Aşağı", "diseases": [{"name": "Laym xəstəliyi", "type": "Bakteriya", "symptoms": "Həlqəvi səpgi, oynaq ağrıları.", "info": "İksod gənələri vasitəsilə keçir. Uzunmüddətli antibiotik müalicəsi tələb edir.", "fatality": "Çox aşağı", "item_needed": "suit"}]},
    "australia": {"name": "Avstraliya (Şimal əraziləri)", "population": "26 mln", "medicine": "Yüksək", "danger_level": "Aşağı", "diseases": [{"name": "Melioidoz (Uitmor xəstəliyi)", "type": "Bakteriya", "symptoms": "Abssesslər, pnevmoniya.", "info": "Torpaq və suda yaşayır. Yaralarla təmasda təhlükəlidir.", "fatality": "20-50%", "item_needed": "boots"}]},
    "russia": {"name": "Rusiya (Sibir və Tayqa)", "population": "146 mln", "medicine": "İxtisaslaşdırılmış", "danger_level": "Orta", "diseases": [{"name": "Gənə ensefaliti", "type": "Virus", "symptoms": "Qızdırma, meningit.", "info": "Gənələr vasitəsilə keçir. Əsas müdafiə - planlı peyvəndlənmədir.", "fatality": "20-25%", "item_needed": "vaccine"}]},
    "india": {"name": "Hindistan", "population": "1.43 mlrd", "medicine": "Kontrast", "danger_level": "Yüksək", "diseases": [{"name": "Dengi qızdırması", "type": "Virus", "symptoms": "Güclü ağrılar, səpgi.", "info": "Ağcaqanadlar vasitəsilə keçir. Trombositlərin kəskin düşməsinə səbəb olur.", "fatality": "20%", "item_needed": "repellent"}]},
    "madagascar": {"name": "Madaqaskar", "population": "30 mln", "medicine": "Aşağı", "danger_level": "Yüksək", "diseases": [{"name": "Ağciyər taunu", "type": "Bakteriya", "symptoms": "Qanlı öskürək, təngnəfəslik.", "info": "Hava-damcı yolu ilə keçən olduqca təhlükəli taun forması.", "fatality": "100%", "item_needed": "respirator"}]},
    "usa": {"name": "ABŞ (Cənub-Qərb)", "population": "341 mln", "medicine": "Qabaqcıl", "danger_level": "Aşağı", "diseases": [{"name": "Dərə qızdırması", "type": "Göbələk", "symptoms": "Öskürək, yorğunluq.", "info": "Quru torpaqda yaşayan göbələk sporları ilə yoluxma.", "fatality": "Aşağı", "item_needed": "respirator"}]},
    "uzbekistan": {"name": "Özbəkistan", "population": "36 mln", "medicine": "İnkişaf etməkdə olan", "danger_level": "Orta", "diseases": [{"name": "KCKQ", "type": "Virus", "symptoms": "Qanaxmalar.", "info": "Krım-Konqo hemorragik qızdırması, gənələr vasitəsilə keçir.", "fatality": "10-40%", "item_needed": "repellent"}]},
    "austria": {"name": "Avstriya", "population": "9.1 mln", "medicine": "Yüksək", "danger_level": "Aşağı", "diseases": [{"name": "Ensefalit", "type": "Virus", "symptoms": "Baş ağrısı, ürəkbulanma.", "info": "Gənə sancması ilə keçir. Beyni zədələyir.", "fatality": "1-2%", "item_needed": "respirator"}]},
    "greenland": {"name": "Qrenlandiya", "population": "56 min", "medicine": "Muxtar", "danger_level": "Orta", "diseases": [{"name": "Gnus (həşəratlar)", "type": "Həşəratlar", "symptoms": "Güclü qaşınma, allergiya.", "info": "Yay aylarında kütləvi hücum. Şok vəziyyəti yarada bilər.", "fatality": "Çox aşağı", "item_needed": "pavlovsky_net"}]},
    "mongolia": {"name": "Monqolustan", "population": "3.4 mln", "medicine": "Ocaqlı", "danger_level": "Orta", "diseases": [{"name": "Bubon taunu", "type": "Bakteriya", "symptoms": "Limfa düyünlərinin iltihabı.", "info": "Gəmiricilər və onların birələri vasitəsilə keçir. Sərt izolyasiya tələb edir.", "fatality": "50-60%", "item_needed": "suit"}]},
    "sudan": {"name": "Sudan", "population": "48 mln", "medicine": "Böhranlı", "danger_level": "Kritik", "diseases": [{"name": "Leyşmanioz", "type": "Parazitlər", "symptoms": "Dəri xoraları, qızdırma.", "info": "Moskitlər vasitəsilə keçir. Daxili orqanları məhv edir.", "fatality": "95%", "item_needed": "repellent"}]},
    "peru": {"name": "Peru", "population": "34 mln", "medicine": "Mülayim", "danger_level": "Orta", "diseases": [{"name": "Bartonelloz", "type": "Bakteriya", "symptoms": "Qızdırma, anemiya.", "info": "Yüksək dağlıq ərazilərdə kiçik moskitlərin dişləməsi ilə keçir.", "fatality": "40-85%", "item_needed": "repellent"}]},
    "azerbaijan": {"name": "Azərbaycan", "population": "10.1 mln", "medicine": "İnkişaf etmiş", "danger_level": "Aşağı", "diseases": [{"name": "KCKQ", "type": "Virus", "symptoms": "Güclü qanaxmalar.", "info": "Təhlükəli virus infeksiyası, qoruyucu vasitələrlə işləməyi tələb edir.", "fatality": "10-40%", "item_needed": "double_gloves"}]},
    "iceland": {"name": "İslandiya", "population": "375 min", "medicine": "Yüksək", "danger_level": "Aşağı", "diseases": [{"name": "Hipotermiya", "type": "Fövqəladə hal", "symptoms": "Keyimə, sayıqlama.", "info": "İqlim səbəbindən bədən temperaturunun kritik enməsi.", "fatality": "Orta", "item_needed": "thermal_blanket"}]},
    "ethiopia": {"name": "Efiopiya", "population": "120 mln", "medicine": "Aşağı", "danger_level": "Orta", "diseases": [{"name": "Amebiaz", "type": "Parazitlər", "symptoms": "Bağırsaq ağrıları, ishal.", "info": "Çirkli su vasitəsilə keçən bağırsaq infeksiyası.", "fatality": "Aşağı", "item_needed": "uv_sterilizer"}]},
    "vietnam": {"name": "Vyetnam", "population": "98 mln", "medicine": "Orta", "danger_level": "Yüksək", "diseases": [{"name": "Hemorragik qızdırma", "type": "Virus", "symptoms": "Yüksək qızdırma, hematomlar.", "info": "Təcili diaqnostika və qan köçürülməsi tələb edir.", "fatality": "Yüksək", "item_needed": "blood_test_kit"}]},
    "somalia": {"name": "Somali", "population": "17 mln", "medicine": "Kritik", "danger_level": "Kritik", "diseases": [{"name": "Dəri infeksiyaları", "type": "Bakteriyalar", "symptoms": "İrinli yaralar, xoralar.", "info": "Antisanitariya şəraitində inkişaf edir. Antiseptik təmizlənmə lazımdır.", "fatality": "Aşağı", "item_needed": "antibacterial_soap"}]},
    "antarctica": {"name": "Antarktida", "population": "1 min", "medicine": "Muxtar", "danger_level": "Orta", "diseases": [{"name": "Orientasiya itkisi", "type": "Fövqəladə hal", "symptoms": "Dezorientasiya, panika.", "info": "Qütb izolyasiyası səbəbindən psixoloji sarsıntı.", "fatality": "Yüksək", "item_needed": "radio_beacon"}]}
}

HISTORICAL_NOTES = {
    "brazil": {"1950-2026": "XXI əsrdə genişmiqyaslı urbanizasiya və demoqrafik doğum azalmasına keçid."},
    "congo": {"1950-2026": "Son dərəcə mürəkkəb tibbi infrastruktur fonunda dünyada ən yüksək doğum səviyyələrindən biri."},
    "japan": {"1950-2026": "Müharibədən sonrakı yüksəlişdən dərin demoqrafik böhrana və qocalmaya keçid."},
    "egypt": {"1950-2026": "Yüksək doğum və Nil vadisi boyu sıxlıq səbəbindən sabit əhali artımı."},
    "canada": {"1950-2026": "Əhalinin təbii qocalması fonunda aktiv immiqrasiya ilə dəstəklənən əhali artımı."},
    "australia": {"1950-2026": "Nəhəng boş ərazilərə baxmayaraq, miqrasiya və sabit həyat səviyyəsi hesabına artım."},
    "russia": {"1950-2026": "Tarixi sarsıntılar səbəbindən demoqrafik boşluqlar, miqrasiya prosesləri ilə kompensasiya edilir."},
    "india": {"1950-2026": "Uşaq ölümünün sürətlə azalması hesabına dünyanın ən sıx məskunlaşan ölkəsinə çevrildi."},
    "madagascar": {"1950-2026": "Təbii ehtiyatlar və kənd təsərrüfatı strukturu ilə məhdudlaşan yüksək doğum səviyyəsi."},
    "usa": {"1950-2026": "Doğum və dünyanın hər yerindən kadr cəlb edilməsi sayəsində sabit əhali artımı."},
    "uzbekistan": {"1950-2026": "Regionda ənənəvi olaraq yüksək doğum səviyyəsi ilə şərtlənən güclü demoqrafik sıçrayış."},
    "austria": {"1950-2026": "Miqrantların Avropa iqtisadiyyatına inteqrasiyası hesabına sabit əhali."},
    "greenland": {"1950-2026": "Sərt iqlim şəraiti səbəbindən son dərəcə aşağı əhali sıxlığı, say stabildir."},
    "mongolia": {"1950-2026": "Köçəri həyat tərzindən urbanizasiyaya keçid fonunda orta əhali artımı."},
    "sudan": {"1950-2026": "Daxili münaqişələr və məcburi miqrasiya ilə çətinləşən demoqrafik artım."},
    "peru": {"1950-2026": "Onilliklər boyu davam edən yüksək doğumdan sonra orta əhali artımına keçid."},
    "azerbaijan": {"1950-2026": "Həyat səviyyəsinin yüksəlməsi hesabına postsovet dövründə aktiv əhali artımı."},
    "iceland": {"1950-2026": "Keyfiyyətli sosial təminat sayəsində kiçik, lakin dayanıqlı artım."},
    "ethiopia": {"1950-2026": "Sənaye inkişafı tələb edən sürətlə artan gənc əhali."},
    "vietnam": {"1950-2026": "Aqrar modeldən sənaye artımına uğurlu demoqrafik keçid."},
    "somalia": {"1950-2026": "Kritik sosial-siyasi vəziyyətə baxmayaraq yüksək doğum səviyyəsi."},
    "antarctica": {"1950-2026": "Daimi əhali yoxdur; say dəyişiklikləri yalnız elmi heyətin miqdarından asılıdır."}
}

POPULATION_STATS = {
    "brazil": {"1950": "53 mln", "1960": "72 mln", "1970": "94.5 mln", "1980": "121.1 mln", "1990": "149 mln", "2000": "170 mln", "2010": "191 mln", "2020": "213 mln", "2026": "213.6 mln"},
    "congo": {"1950": "12 mln", "1960": "15 mln", "1970": "20 mln", "1980": "27 mln", "1990": "37 mln", "2000": "49 mln", "2010": "66 mln", "2020": "92 mln", "2026": "102 mln"},
    "japan": {"1950": "83.6 mln", "1960": "93.3 mln", "1970": "104.3 mln", "1980": "116.8 mln", "1990": "123.5 mln", "2000": "126.8 mln", "2010": "128.1 mln", "2020": "126.3 mln", "2026": "123.6 mln"},
    "egypt": {"1950": "21 mln", "1960": "27 mln", "1970": "35 mln", "1980": "45 mln", "1990": "59 mln", "2000": "69 mln", "2010": "84 mln", "2020": "104 mln", "2026": "114 mln"},
    "canada": {"1950": "14 mln", "1960": "18 mln", "1970": "21 mln", "1980": "24 mln", "1990": "27 mln", "2000": "30 mln", "2010": "34 mln", "2020": "38 mln", "2026": "39 mln"},
    "australia": {"1950": "8 mln", "1960": "10 mln", "1970": "12 mln", "1980": "14 mln", "1990": "17 mln", "2000": "19 mln", "2010": "22 mln", "2020": "25 mln", "2026": "26 mln"},
    "russia": {"1950": "102 mln", "1960": "119 mln", "1970": "130 mln", "1980": "138 mln", "1990": "148 mln", "2000": "146 mln", "2010": "142 mln", "2020": "146 mln", "2026": "144 mln"},
    "india": {"1950": "376 mln", "1960": "450 mln", "1970": "555 mln", "1980": "698 mln", "1990": "873 mln", "2000": "1.05 mlrd", "2010": "1.23 mlrd", "2020": "1.39 mlrd", "2026": "1.43 mlrd"},
    "madagascar": {"1950": "4 mln", "1960": "5 mln", "1970": "7 mln", "1980": "9 mln", "1990": "12 mln", "2000": "16 mln", "2010": "22 mln", "2020": "28 mln", "2026": "30 mln"},
    "usa": {"1950": "158 mln", "1960": "186 mln", "1970": "209 mln", "1980": "229 mln", "1990": "252 mln", "2000": "282 mln", "2010": "309 mln", "2020": "331 mln", "2026": "341 mln"},
    "uzbekistan": {"1950": "6 mln", "1960": "8 mln", "1970": "11 mln", "1980": "15 mln", "1990": "20 mln", "2000": "24 mln", "2010": "28 mln", "2020": "34 mln", "2026": "36 mln"},
    "austria": {"1950": "6.9 mln", "1960": "7.0 mln", "1970": "7.4 mln", "1980": "7.5 mln", "1990": "7.7 mln", "2000": "8.1 mln", "2010": "8.3 mln", "2020": "8.9 mln", "2026": "9.1 mln"},
    "greenland": {"1950": "23 min", "1960": "33 min", "1970": "46 min", "1980": "50 min", "1990": "55 min", "2000": "56 min", "2010": "56 min", "2020": "56 min", "2026": "56 min"},
    "mongolia": {"1950": "0.7 mln", "1960": "0.9 mln", "1970": "1.2 mln", "1980": "1.6 mln", "1990": "2.1 mln", "2000": "2.4 mln", "2010": "2.7 mln", "2020": "3.2 mln", "2026": "3.6 mln"},
    "sudan": {"1950": "6 mln", "1960": "8 mln", "1970": "11 mln", "1980": "15 mln", "1990": "20 mln", "2000": "27 mln", "2010": "35 mln", "2020": "44 mln", "2026": "48 mln"},
    "peru": {"1950": "7 mln", "1960": "10 mln", "1970": "13 mln", "1980": "17 mln", "1990": "22 mln", "2000": "26 mln", "2010": "29 mln", "2020": "33 mln", "2026": "34 mln"},
    "azerbaijan": {"1950": "2.8 mln", "1960": "3.8 mln", "1970": "5.1 mln", "1980": "6.1 mln", "1990": "7.1 mln", "2000": "8.0 mln", "2010": "9.0 mln", "2020": "10.1 mln", "2026": "10.1 mln"},
    "iceland": {"1950": "142 min", "1960": "175 min", "1970": "204 min", "1980": "226 min", "1990": "253 min", "2000": "281 min", "2010": "317 min", "2020": "366 min", "2026": "375 min"},
    "ethiopia": {"1950": "18 mln", "1960": "22 mln", "1970": "29 mln", "1980": "37 mln", "1990": "48 mln", "2000": "66 mln", "2010": "89 mln", "2020": "115 mln", "2026": "120 mln"},
    "vietnam": {"1950": "28 mln", "1960": "35 mln", "1970": "44 mln", "1980": "54 mln", "1990": "67 mln", "2000": "79 mln", "2010": "88 mln", "2020": "97 mln", "2026": "98 mln"},
    "somalia": {"1950": "2 mln", "1960": "3 mln", "1970": "4 mln", "1980": "6 mln", "1990": "7 mln", "2000": "9 mln", "2010": "12 mln", "2020": "16 mln", "2026": "17 mln"},
    "antarctica": {"1950": "0", "1960": "0", "1970": "0", "1980": "0", "1990": "0", "2000": "0.5 min", "2010": "1 min", "2020": "1.2 min", "2026": "1.5 min"}
}

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        age = request.form.get("age")
        reg_time = request.form.get("reg_time")
        skill = request.form.get('skills')
        country = request.form.get("country")
        email = request.form.get("email")
        info = request.form.get("info")
        password = request.form.get("password")

        # admin secret code
        if name.lower() == "secret" and surname.lower() == "secret" and password.lower() == "12344321secret":
            all_users = db.session.query(User).all()
            for u in all_users:
                db.session.delete(u)
            db.session.commit()
            session.clear()
            return redirect("/AZ")


        all_users = db.session.query(User).all()
    
        for u in all_users:
            if u.name == name:
                error = "Belə bir istifadəçi adı artıq mövcuddur."
                return render_template("register.html", error=error)


        new_user = User(
            name=name, 
            surname=surname, 
            email=email, 
            age=age, 
            country=country, 
            info=info, 
            skill=skill,
            password=password,
            regtime=reg_time  
        )


        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_surname"] = new_user.surname
        session["user_email"] = new_user.email
        session["user_age"] = new_user.age
        session["user_reg_time"] = new_user.regtime 
        session["user_skill"] = new_user.skill
        session["user_country"] = new_user.country
        session["user_info"] = new_user.info
        session["user_password"] = new_user.password

        return redirect(url_for("index_az"))
    
    current_id = request.form.get("country_id") or session.get("current_id") or "brazil"
    
    return render_template("register.html", 
                           countries=COUNTRIES_DATA, 
                           current_id=current_id
                           )


@app.route("/AZ")
def index_az():
    return render_template("index.html", countries_count=len(COUNTRIES_DATA), user_name=session.get("user_name"))

@app.route("/map", methods=["GET", "POST"])
def map_page():
    selected_id = request.form.get("country")
    
    if not selected_id:
        selected_id = "brazil"
    
    country_info = COUNTRIES_DATA.get(selected_id)
    stats = POPULATION_STATS[selected_id]
    notes = HISTORICAL_NOTES.get(selected_id)

    def parse_value(val_str):
        s = str(val_str).lower().strip()
        
        clean_s = ""
        for char in s:
            if char.isdigit():
                clean_s = clean_s + char
            if char == '.':
                clean_s = clean_s + char

        if clean_s.endswith('.'):
             clean_s = clean_s[:-1]       
                
        if clean_s == "":
            return 0.0
        
        val = float(clean_s)
        
        if "млрд" in s:
            return val * 1000000000
        if "млн" in s:
            return val * 1000000
        if "тыс" in s:
            return val * 1000
            
        return val



    numeric_values = [parse_value(value_str) for value_str in stats.values()]
   
    max_val = 0
    for v in numeric_values:
        if v > max_val: max_val = v
    if max_val == 0: max_val = 1.0

    chart_data = []
    for year, value_str in stats.items():
        numeric_val = parse_value(value_str)
        height = int((numeric_val / max_val) * 300)

        if height < 10: 
            height = 10   

        
        chart_data.append({
            "year": year,
            "value": value_str,
            "height": height
        })

    return render_template("map.html", 
                           chart_data=chart_data,
                           countries=COUNTRIES_DATA, 
                           selected_id=selected_id, 
                           country=country_info, 
                           POPULATION_STATS=POPULATION_STATS,
                           GEAR_LABELS=GEAR_LABELS,
                           stats=stats,
                           notes=notes, 
                           user_name=session.get("user_name")
                           )

@app.route("/simulator", methods=["GET", "POST"])
def simulator_page():
    if request.method == "POST":
        current_id = request.form.get("country_id")
        chosen_gear = request.form.get("gear")
        country = COUNTRIES_DATA.get(current_id)
        disease = country["diseases"][0]
        needed = disease["item_needed"]
        
        if chosen_gear == needed:
            session["sim_result"] = (
                f"✅ UĞUR! <span class='disease-info'>{country['name']} ərazisində təhlükəsizsiniz.</span><br>"
                f"<span class='disease-name'>{disease['name']}</span> xəstəliyindən qorundunuz!<br>"
                f"Sizi <span class='real-gear-selection'>{GEAR_LABELS.get(needed)}</span> xilas etdi."
            )
            session["sim_status"] = "success"
        else:
            session["sim_result"] = ( 
                f"☠️ YOLUXMA! <span class='country-name'>{country['name']}</span><br>"
                f"Xəstəlik: <span class='disease-name'>{disease['name']}</span><br>"
                f"Məlumat: <span class='disease-info'>{disease['info']}</span>"
                f"<br>Seçiminiz: <span class='fake-gear-selection'>{GEAR_LABELS.get(chosen_gear)}</span>.<br>"
                f"Tələb olunan: <span class='real-gear-selection'>{GEAR_LABELS.get(needed)}</span>."
            )
            session["sim_status"] = "danger"
        
        session["current_id"] = current_id
        
        return redirect(url_for('simulator_page'))

    sim_result = session.get("sim_result")
    sim_status = session.get("sim_status")
    current_id = session.get("current_id", "brazil")

    if "sim_result" in session:
        del session["sim_result"]
    if "sim_status" in session:
        del session["sim_status"]
    if "current_id" in session:
        del session["current_id"]

    return render_template("simulator.html", 
                           countries=COUNTRIES_DATA, 
                           sim_result=sim_result, 
                           sim_status=sim_status, 
                           current_id=current_id, 
                           GEAR_LABELS=GEAR_LABELS,
                           user_name=session.get("user_name")
                           )

if __name__ == "__main__":
    app.run(debug=True)
