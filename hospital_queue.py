from flask import Flask, render_template, request, redirect

app = Flask(__name__)

class Node:
    def __init__(self, name, age, queue_number, doctor_type):
        self.name = name
        self.age = age
        self.queue_number = queue_number
        self.doctor_type = doctor_type
        self.next = None
        self.prev = None

class HospitalQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, name, age, doctor_type):
        # Membuat nomor antrian baru
        if self.tail is None:
            queue_number = 1
        else:
            queue_number = self.tail.queue_number + 1
        
        # Membuat node baru
        new_node = Node(name, age, queue_number, doctor_type)

        if self.tail is None:
            self.head = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail

        self.tail = new_node
        print(f"Antrian {new_node.queue_number} untuk {new_node.name} ({new_node.age} tahun, {new_node.doctor_type}) ditambahkan.")

    def dequeue(self):
        if self.head is None:
            print("Antrian kosong.")
            return

        removed_node = self.head
        self.head = self.head.next

        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None

        print(f"Antrian {removed_node.queue_number} untuk {removed_node.name} ({removed_node.age} tahun, {removed_node.doctor_type}) dilayani dan dihapus.")

    def peek(self):
        if self.head is None:
            print("Antrian kosong.")
        else:
            print(f"Antrian berikutnya: {self.head.queue_number} - {self.head.name} ({self.head.age} tahun, {self.head.doctor_type})")

    def display(self):
        current = self.head
        if current is None:
            print("Antrian kosong.")
        else:
            print("Daftar Antrian:")
            while current is not None:
                print(f"{current.queue_number} - {current.name} ({current.age} tahun, {current.doctor_type})")
                current = current.next

# Membuat objek antrian rumah sakit
queue = HospitalQueue()

@app.route('/')
def index():
    patients = []
    current = queue.head
    while current is not None:
        patients.append(current)
        current = current.next
    return render_template('index.html', patients=patients)

@app.route('/enqueue', methods=['POST'])
def enqueue():
    name = request.form['name']
    age = request.form['age']
    doctor_type = request.form['doctor_type']
    queue.enqueue(name, age, doctor_type)
    return redirect('/')

@app.route('/dequeue', methods=['POST'])
def dequeue():
    queue.dequeue()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
