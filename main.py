#!/usr/bin/env python
# Clinic Scheduler - Simple Menu System

def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the application header."""
    print("=" * 50)
    print("           CLINIC SCHEDULER SYSTEM")
    print("=" * 50)
    print()

# Main login menu
def display_login_menu():
    clear_screen()
    display_header()
    print("LOGIN MENU")
    print("1. Login sebagai Admin")
    print("2. Login sebagai Dokter")
    print("3. Login sebagai Pasien")
    print("4. Keluar")
    print()

# Authentication function (placeholder)
def authenticate(role):
    clear_screen()
    display_header()
    print(f"LOGIN SEBAGAI {role.upper()}")
    print("-" * 30)
    username = input("Username: ")
    password = input("Password: ")

    # This is just a placeholder, actual authentication would be implemented later
    if username and password:
        print(f"\nLogin sebagai {role} berhasil!")
        input("Tekan Enter untuk melanjutkan...")
        return True
    else:
        print("\nLogin gagal. Username atau password salah.")
        input("Tekan Enter untuk kembali...")
        return False

# Admin menu
def display_admin_menu():
    while True:
        clear_screen()
        display_header()
        print("MENU ADMIN")
        print("-" * 30)
        print("1. Tambah Jadwal Dokter (Create)")
        print("2. Lihat Jadwal Dokter (Read)")
        print("3. Update Jadwal Dokter (Update)")
        print("4. Hapus Jadwal Dokter (Delete)")
        print("5. Cari Jadwal Dokter (Search)")
        print("6. Lihat Antrian Pasien")
        print("7. Logout")
        print()

        choice = input("Pilih menu (1-7): ")

        if choice == '1':
            print("Fitur Tambah Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '2':
            print("Fitur Lihat Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '3':
            print("Fitur Update Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '4':
            print("Fitur Hapus Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '5':
            print("Fitur Cari Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '6':
            print("Fitur Lihat Antrian Pasien akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '7':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")

# Doctor menu
def display_doctor_menu():
    while True:
        clear_screen()
        display_header()
        print("MENU DOKTER")
        print("-" * 30)
        print("1. Lihat Jadwal Saya")
        print("2. Lihat Antrian Pasien Saya")
        print("3. Logout")
        print()

        choice = input("Pilih menu (1-3): ")

        if choice == '1':
            print("Fitur Lihat Jadwal Saya akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '2':
            print("Fitur Lihat Antrian Pasien Saya akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '3':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")

# Patient menu
def display_patient_menu():
    while True:
        clear_screen()
        display_header()
        print("MENU PASIEN")
        print("-" * 30)
        print("1. Lihat Jadwal Dokter")
        print("2. Cari Dokter")
        print("3. Daftar Antrian")
        print("4. Logout")
        print()

        choice = input("Pilih menu (1-4): ")

        if choice == '1':
            print("Fitur Lihat Jadwal Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '2':
            print("Fitur Cari Dokter akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '3':
            print("Fitur Daftar Antrian akan diimplementasikan.")
            input("Tekan Enter untuk kembali...")
        elif choice == '4':
            print("Logout berhasil.")
            break
        else:
            print("Pilihan tidak valid.")
            input("Tekan Enter untuk kembali...")

# Main function
def main():
    while True:
        display_login_menu()
        choice = input("Pilih menu (1-4): ")

        if choice == '1':  # Admin
            if authenticate("Admin"):
                display_admin_menu()
        elif choice == '2':  # Doctor
            if authenticate("Dokter"):
                display_doctor_menu()
        elif choice == '3':  # Patient
            if authenticate("Pasien"):
                display_patient_menu()
        elif choice == '4':  # Exit
            clear_screen()
            print("Terima kasih telah menggunakan Clinic Scheduler System.")
            print("Sampai jumpa kembali!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            input("Tekan Enter untuk kembali...")

if __name__ == "__main__":
    main()
