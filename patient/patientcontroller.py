def book_appointment(doctors, patient):
    print("\n=== Booking Jadwal ===")
    available = []
    for i, doc in enumerate(doctors):
        for j, sched in enumerate(doc.schedule):
            if not sched.booked:
                print(f"{len(available)+1}. Dr. {doc.name} ({doc.specialty}) | {sched.date}, {sched.time}")
                available.append((doc, sched))
    
    if not available:
        print("Tidak ada jadwal yang tersedia untuk dibooking.")
        return

    try:
        choice = int(input("Pilih jadwal (nomor): ")) - 1
        if choice < 0 or choice >= len(available):
            print("Pilihan tidak valid.")
            return
        selected_doc, selected_sched = available[choice]
        selected_sched.booked = True
        selected_sched.patient = patient
        patient.bookings.append({
            "doctor": selected_doc.name,
            "specialty": selected_doc.specialty,
            "date": selected_sched.date,
            "time": selected_sched.time
        })
        print("Booking berhasil!")
    except ValueError:
        print("Input tidak valid.")


def patient_menu(patient, doctors):
    while True:
        print("\n=== Menu Pasien ===")
        print("1. Cari Jadwal Dokter")
        print("2. Booking Jadwal")
        print("3. Lihat Riwayat Booking")
        print("4. Logout")
        choice = input("Pilih menu: ")

        if choice == '1':
            print("\n=== Jadwal Dokter Tersedia ===")
            found = False
            for doc in doctors:
                for sched in doc.schedule:
                    if not sched.booked:
                        print(f"- Dr. {doc.name} ({doc.specialty}) | {sched.date}, {sched.time}")
                        found = True
            if not found:
                print("Tidak ada jadwal yang tersedia saat ini.")

        elif choice == '2':
            book_appointment(doctors, patient)

        elif choice == '3':
            print("\n=== Riwayat Booking ===")
            if not patient.bookings:
                print("Belum ada booking.")
            else:
                for i, b in enumerate(patient.bookings, 1):
                    print(f"{i}. Dr. {b['doctor']} ({b['specialty']}) | {b['date']}, {b['time']}")

        elif choice == '4':
            print("Logout berhasil.\n")
            break

        else:
            print("Pilihan tidak valid.")
