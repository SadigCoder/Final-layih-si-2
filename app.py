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

POPULATION_STATS = {
    "brazil": {"1950": "53 млн", "1960": "72 млн", "1970": "94.5 млн", "1980": "121.1 млн", "1990": "149 млн", "2000": "170 млн", "2010": "191 млн", "2020": "213 млн", "2026": "213.6 млн"},
    "congo": {"1950": "12 млн", "1960": "15 млн", "1970": "20 млн", "1980": "27 млн", "1990": "37 млн", "2000": "49 млн", "2010": "66 млн", "2020": "92 млн", "2026": "102 млн"},
    "japan": {"1950": "83.6 млн", "1960": "93.3 млн", "1970": "104.3 млн", "1980": "116.8 млн", "1990": "123.5 млн", "2000": "126.8 млн", "2010": "128.1 млн", "2020": "126.3 млн", "2026": "123.6 млн"},
    "egypt": {"1950": "21 млн", "1960": "27 млн", "1970": "35 млн", "1980": "45 млн", "1990": "59 млн", "2000": "69 млн", "2010": "84 млн", "2020": "104 млн", "2026": "114 млн"},
    "canada": {"1950": "14 млн", "1960": "18 млн", "1970": "21 млн", "1980": "24 млн", "1990": "27 млн", "2000": "30 млн", "2010": "34 млн", "2020": "38 млн", "2026": "39 млн"},
    "australia": {"1950": "8 млн", "1960": "10 млн", "1970": "12 млн", "1980": "14 млн", "1990": "17 млн", "2000": "19 млн", "2010": "22 млн", "2020": "25 млн", "2026": "26 млн"},
    "russia": {"1950": "102 млн", "1960": "119 млн", "1970": "130 млн", "1980": "138 млн", "1990": "148 млн", "2000": "146 млн", "2010": "142 млн", "2020": "146 млн", "2026": "144 млн"},
    "india": {"1950": "376 млн", "1960": "450 млн", "1970": "555 млн", "1980": "698 млн", "1990": "873 млн", "2000": "1.05 млрд", "2010": "1.23 млрд", "2020": "1.39 млрд", "2026": "1.43 млрд"},
    "madagascar": {"1950": "4 млн", "1960": "5 млн", "1970": "7 млн", "1980": "9 млн", "1990": "12 млн", "2000": "16 млн", "2010": "22 млн", "2020": "28 млн", "2026": "30 млн"},
    "usa": {"1950": "158 млн", "1960": "186 млн", "1970": "209 млн", "1980": "229 млн", "1990": "252 млн", "2000": "282 млн", "2010": "309 млн", "2020": "331 млн", "2026": "341 млн"},
    "uzbekistan": {"1950": "6 млн", "1960": "8 млн", "1970": "11 млн", "1980": "15 млн", "1990": "20 млн", "2000": "24 млн", "2010": "28 млн", "2020": "34 млн", "2026": "36 млн"},
    "austria": {"1950": "6.9 млн", "1960": "7.0 млн", "1970": "7.4 млн", "1980": "7.5 млн", "1990": "7.7 млн", "2000": "8.1 млн", "2010": "8.3 млн", "2020": "8.9 млн", "2026": "9.1 млн"},
    "greenland": {"1950": "23 тыс.", "1960": "33 тыс.", "1970": "46 тыс.", "1980": "50 тыс.", "1990": "55 тыс.", "2000": "56 тыс.", "2010": "56 тыс.", "2020": "56 тыс.", "2026": "56 тыс."},
    "mongolia": {"1950": "0.7 млн", "1960": "0.9 млн", "1970": "1.2 млн", "1980": "1.6 млн", "1990": "2.1 млн", "2000": "2.4 млн", "2010": "2.7 млн", "2020": "3.2 млн", "2026": "3.6 млн"},
    "sudan": {"1950": "6 млн", "1960": "8 млн", "1970": "11 млн", "1980": "15 млн", "1990": "20 млн", "2000": "27 млн", "2010": "35 млн", "2020": "44 млн", "2026": "48 млн"},
    "peru": {"1950": "7 млн", "1960": "10 млн", "1970": "13 млн", "1980": "17 млн", "1990": "22 млн", "2000": "26 млн", "2010": "29 млн", "2020": "33 млн", "2026": "34 млн"},
    "azerbaijan": {"1950": "2.8 млн", "1960": "3.8 млн", "1970": "5.1 млн", "1980": "6.1 млн", "1990": "7.1 млн", "2000": "8.0 млн", "2010": "9.0 млн", "2020": "10.1 млн", "2026": "10.1 млн"},
    "iceland": {"1950": "142 тыс.", "1960": "175 тыс.", "1970": "204 тыс.", "1980": "226 тыс.", "1990": "253 тыс.", "2000": "281 тыс.", "2010": "317 тыс.", "2020": "366 тыс.", "2026": "375 тыс."},
    "ethiopia": {"1950": "18 млн", "1960": "22 млн", "1970": "29 млн", "1980": "37 млн", "1990": "48 млн", "2000": "66 млн", "2010": "89 млн", "2020": "115 млн", "2026": "120 млн"},
    "vietnam": {"1950": "28 млн", "1960": "35 млн", "1970": "44 млн", "1980": "54 млн", "1990": "67 млн", "2000": "79 млн", "2010": "88 млн", "2020": "97 млн", "2026": "98 млн"},
    "somalia": {"1950": "2 млн", "1960": "3 млн", "1970": "4 млн", "1980": "6 млн", "1990": "7 млн", "2000": "9 млн", "2010": "12 млн", "2020": "16 млн", "2026": "17 млн"},
    "antarctica": {"1950": "0", "1960": "0", "1970": "0", "1980": "0", "1990": "0", "2000": "0.5 тыс.", "2010": "1 тыс.", "2020": "1.2 тыс.", "2026": "1.5 тыс."}
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


if __name__ == "__main__":
    app.run(debug=True)