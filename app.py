import streamlit as st
import pandas as pd
import io
from supabase import create_client, Client

# Page Config
st.set_page_config(page_title="AkademIQ v2 - Sınav ve Kazanım Analiz Sistemi", layout="wide", page_icon="🎓")

# Supabase Connection
@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_supabase()
except Exception as e:
    st.error("Supabase bağlantısı kurulamadı. Lütfen .streamlit/secrets.toml dosyasını kontrol edin.")
    st.stop()

# Session State Setup
if "user" not in st.session_state:
    st.session_state["user"] = None

# --- AUTHENTICATION ---
def login():
    st.markdown("<h1 style='text-align: center;'>🎓 AkademIQ v2</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Giriş Paneli</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı / Öğrenci No")
            password = st.text_input("Şifre", type="password")
            submit = st.form_submit_button("Giriş Yap", use_container_width=True)
            
            if submit:
                res = supabase.table("users").select("*").eq("username", username).eq("password_hash", password).execute()
                if res.data:
                    st.session_state["user"] = res.data[0]
                    st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("Hatalı kullanıcı adı veya şifre!")

def logout():
    st.session_state["user"] = None
    st.rerun()

# --- ADMIN PANEL: EXCEL TEMPLATES ---
def generate_student_excel_template():
    df = pd.DataFrame({
        "öğrenci_no": ["101", "102"],
        "ad_soyad": ["Ahmet Yılmaz", "Ayşe Kaya"],
        "sınıf_şube": ["12-A", "8-B"],
        "alan": ["SAY", "LGS"],
        "veli_kullanıcı_adı": ["veli_101", "veli_102"],
        "veli_şifre": ["123456", "123456"],
        "veli_ad_soyad": ["Mehmet Yılmaz", "Fatma Kaya"],
        "veli_telefon": ["05551112233", "05552223344"],
        "öğrenci_şifre": ["123456", "123456"]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Öğrenci_Veli_Listesi")
    return output.getvalue()

def generate_teacher_excel_template():
    df = pd.DataFrame({
        "kullanıcı_adı": ["mat_ahmet", "turkce_elife"],
        "şifre": ["123456", "123456"],
        "ad_soyad": ["Ahmet Öğretmen", "Elif Öğretmen"],
        "sınıf_şube": ["12-A", "8-B"],
        "ders": ["Matematik", "Türkçe"]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Öğretmen_Listesi")
    return output.getvalue()

# --- ADMIN PANEL ---
def admin_panel():
    st.sidebar.title("🛠️ Admin Paneli")
    st.sidebar.write(f"Hoş geldiniz, **{st.session_state['user']['full_name']}**")
    if st.sidebar.button("Çıkış Yap"):
        logout()
        
    menu = st.sidebar.radio("Menü", ["Öğrenci & Veli Yükle", "Öğretmen Yükle", "Kullanıcı Listesi"])
    
    if menu == "Öğrenci & Veli Yükle":
        st.header("📥 Öğrenci ve Veli Bilgilerini Toplu Yükleme")
        st.info("Aşağıdaki butondan standart şablonu indirip doldurduktan sonra sisteme yükleyebilirsiniz.")
        
        template = generate_student_excel_template()
        st.download_button(
            label="📄 Öğrenci & Veli Excel Şablonunu İndir",
            data=template,
            file_name="AkademIQ_Ogrenci_Veli_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        uploaded_file = st.file_uploader("Doldurulmuş Excel Dosyasını Yükleyin", type=["xlsx", "xls"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.write("📌 Yüklenen Veri Önizlemesi:", df.head())
            
            if st.button("Verileri Sisteme Aktar"):
                success_count = 0
                for _, row in df.iterrows():
                    try:
                        # 1. Create Parent User
                        parent_res = supabase.table("users").insert({
                            "username": str(row["veli_kullanıcı_adı"]),
                            "password_hash": str(row["veli_şifre"]),
                            "full_name": str(row["veli_ad_soyad"]),
                            "role": "parent"
                        }).execute()
                        parent_id = parent_res.data[0]["id"] if parent_res.data else None

                        # 2. Create Student User
                        student_user_res = supabase.table("users").insert({
                            "username": str(row["öğrenci_no"]),
                            "password_hash": str(row["öğrenci_şifre"]),
                            "full_name": str(row["ad_soyad"]),
                            "role": "student"
                        }).execute()
                        student_id = student_user_res.data[0]["id"] if student_user_res.data else None

                        # 3. Insert Student Details
                        supabase.table("student_details").insert({
                            "student_no": str(row["öğrenci_no"]),
                            "user_id": student_id,
                            "grade_class": str(row["sınıf_şube"]),
                            "branch_type": str(row["alan"]),
                            "parent_user_id": parent_id,
                            "phone": str(row["veli_telefon"])
                        }).execute()
                        
                        success_count += 1
                    except Exception as e:
                        st.error(f"Hata ({row['ad_soyad']}): {e}")
                
                st.success(f"✅ Toplam {success_count} öğrenci ve veli başarıyla kaydedildi!")

    elif menu == "Öğretmen Yükle":
        st.header("👨‍🏫 Öğretmen Bilgilerini Toplu Yükleme")
        template = generate_teacher_excel_template()
        st.download_button(
            label="📄 Öğretmen Excel Şablonunu İndir",
            data=template,
            file_name="AkademIQ_Ogretmen_Sablonu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        uploaded_file = st.file_uploader("Doldurulmuş Excel Dosyasını Yükleyin", type=["xlsx", "xls"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.write("📌 Yüklenen Veri Önizlemesi:", df.head())
            
            if st.button("Öğretmenleri Kaydet"):
                for _, row in df.iterrows():
                    try:
                        teacher_res = supabase.table("users").insert({
                            "username": str(row["kullanıcı_adı"]),
                            "password_hash": str(row["şifre"]),
                            "full_name": str(row["ad_soyad"]),
                            "role": "teacher"
                        }).execute()
                        
                        if teacher_res.data:
                            t_id = teacher_res.data[0]["id"]
                            supabase.table("teacher_classes").insert({
                                "teacher_user_id": t_id,
                                "grade_class": str(row["sınıf_şube"]),
                                "subject": str(row["ders"])
                            }).execute()
                    except Exception as e:
                        st.error(f"Hata ({row['ad_soyad']}): {e}")
                st.success("✅ Öğretmenler ve sınıf atamaları eklendi!")

    elif menu == "Kullanıcı Listesi":
        st.header("👥 Sistemdeki Kullanıcılar")
        res = supabase.table("users").select("username, full_name, role, created_at").execute()
        if res.data:
            st.dataframe(pd.DataFrame(res.data), use_container_width=True)

# --- MAIN CONTROLLER ---
user = st.session_state["user"]
if user is None:
    login()
else:
    role = user["role"]
    if role == "admin":
        admin_panel()
    elif role == "teacher":
        st.sidebar.title("👨‍🏫 Öğretmen Paneli")
        st.write("Öğretmen modülü hazırlanıyor...")
        if st.sidebar.button("Çıkış"): logout()
    elif role == "student":
        st.sidebar.title("🎓 Öğrenci Paneli")
        st.write("Öğrenci modülü hazırlanıyor...")
        if st.sidebar.button("Çıkış"): logout()
    elif role == "parent":
        st.sidebar.title("👨‍👩‍👧 Veli Paneli")
        st.write("Veli modülü hazırlanıyor...")
        if st.sidebar.button("Çıkış"): logout()