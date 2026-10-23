import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_change_this_in_production'

# Thư mục lưu trữ file ảo (Cloud storage folder)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Quản lý Key kích hoạt và quyền hạn
# Admin Key mặc định có quyền miễn phí và quản trị
ADMIN_KEY = "ADMIN_MASTER_KEY_2026"
VALID_KEYS = {
    ADMIN_KEY: "admin",
    "VIP-SAMPLE-KEY-123": "user" # Key mẫu cho khách hàng
}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = request.form.get('key').strip()
        if key in VALID_KEYS:
            session['user'] = key
            session['role'] = VALID_KEYS[key]
            flash('Đăng nhập hệ thống Cloud thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Key không hợp lệ hoặc chưa thanh toán! Vui lòng kiểm tra lại.', 'danger')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    role = session.get('role', 'user')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Không tìm thấy file tải lên', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Chưa chọn file', 'danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f'Upload file thành công: {filename}', 'success')
            return redirect(url_for('dashboard'))

    # Lấy danh sách file trên cloud
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dashboard.html', files=files, role=role)

@app.route('/download/<filename>')
def download(filename):
    if 'user' not in session:
        return redirect(url_for('login'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/add_key', methods=['POST'])
def add_key():
    if 'user' not in session or session.get('role') != 'admin':
        flash('Bạn không có quyền thực hiện thao tác này!', 'danger')
        return redirect(url_for('dashboard'))
    
    new_key = request.form.get('new_key').strip()
    if new_key:
        VALID_KEYS[new_key] = 'user'
        flash(f'Đã cấp key mới thành công: {new_key}', 'success')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
