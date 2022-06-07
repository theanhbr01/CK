Remote Desktop with Gmail

1. Giới thiệu
Chúng ta sẽ sử dụng kiểu Json để gửi đi request và nhận response

Format request
{
    'Method': 'Method' //Mã của chức năng điều khiển
    'Data': { 
        //Tùy vào mỗi chức năng sẽ có một data nhất định
    }
}

Format response
{
    'isSuccess': True // Thông báo thành công/thất bại
    'message': //Nếu thành công sẽ trả ra kết quả. Ngược lại sẽ trả về lỗi
}

2. Email Template
EmailTemplate được viết dưới dạng class để control phần gửi và nhận email. Phần mail này được gắn cứng các endpoint, port của gmail. Có thể thay đổi thành các server mail khác.
    2.1 Khởi tạo
        EmailTemplate(userName, password)
    2.2 Nhận mail 
        Nhận mail chỉ trả về những mail chưa đọc
        EmailTemplate.Receive() trả về một string converted json bao gồm các thông tin:
        - From (Email người gửi)
        - Subject (Tiêu đề mail)
        - Body (Nội dung mail)
        - FileAttachment (Tên file đính kèm, khi nhận mail server sẽ tự tải xuống ./Downloads)
    Ex: {
        'From': 'test@gmail.com',
        'Subject': 'Email Subject Test',
        'Body': 'Email Body Test',
        'FileAttachment': 'File.zip'
    }
    2.3 Gửi mail
        EmailTemplate.SendNotification(emailFrom, emailTo, emailCc, emailBcc, emailReplyTo, subject, body, fileName, filePath) để gửi mail với các nội dung:
        - emailFrom (Tên người gửi mail, mặc định là mail của server) *Bắt buộc
        - emailTo (email người nhận) *Bắt buộc
        - emailCc (email được CC đến)
        - emailBcc (email được BCC đến)
        - emailReplyTo (email được reply)
        - subject (Tiêu đề mail)
        - body (Nội dung mail)
        - fileName (Tên file đính kèm)
        - filePath (Đường dẫn file trên server)
3. Chức năng remote
    Các chức năng được viết dưới static class để control và nằm ở trong ./Controls
    3.1 Hiển thị các Process và App
        File: ./Controls/AppProcessServerControl.py
        Method: APPS

        Chức năng này hiển thị các process, app đang chạy
        3.1.1 Hiển thị các Process
            Data request format:
            {
                'Action': 'SHOW'
                'Status': 'PROCESS'
            }

        3.1.2 Hiển thị các App
            Data request format:
            {
                'Action': 'SHOW'
                'Status': 'APP' 
            }

    3.2 Stop hoặc kill một process hoặc app
        File: ./Controls/AppProcessServerControl.py
        Method: APPS

        Chức năng này Stop hoặc kill một process, app đang chạy

        Data request format:
        {
            'Action': 'KILL'
            'ID': 'ID' // Mã của process/app cần thực hiện chức năng
        }

    3.3 Shutdown / Restart
        File: ./Controls/ShutdownRestartControl.py
        Method: SHUTDOWN
        Chức năng này Stop hoặc kill một process, app đang chạy

        3.3.1 ShutDown
            Data request format:
            {
                'Action': 'SHUTDOWN'
            }

        3.3.2 Restart
            Data request format:
            {
                'Action': 'RESTART'
            }
    3.4 Chụp màn hình hiện thời
        File: ./Controls/ScreenshotControl.py
        Method: SCREENSHOT
        Chức năng này để chụp màn hình hiện thời

        Trong mail response sẽ đính kèm một tệp ảnh màn hình hiện thời
    3.5 Cập nhật giá trị 1 entry trong registry
        File: ./Controls/RegistryControl.py
        Method: REGISTRY
        Chức năng này để cập nhật giá trị 1 entry trong registry

        3.5.1 Tạo một registry
            Data request format:
            {
                'ID': 0
                'path': '' //Đường dẫn file lưu registry
            }
        3.5.2 Lấy giá trị một entry
            Data request format:
            {
                'ID': 1
                'path': '' //Đường dẫn file registry
                'name_value': '' //Tên giá trị entry
            }
        3.5.3 Cập nhật giá trị một entry
            Data request format:
            {
                'ID': 2
                'path': '' //Đường dẫn file registry
                'name_value': '' //Tên giá trị entry
                'value': '' //Giá trị entry
                'v_type': '' //Kiểu giá trị 
                
            }
        3.5.4 Tạo một entry
            Data request format:
            {
                'ID': 3
                'path': '' //Đường dẫn file registry
            }
        3.5.4 Xóa một entry
            Data request format:
            {
                'ID': 4
                'path': '' //Đường dẫn file registry
            }
    3.6 Bắt phím nhận
        File: ./Controls/KeyloggerControl.py
        Method: KEYLOG
        Chức năng này để bắt phím nhận

        3.6.1 Bắt đầu
            Data request format:
            {
                'Action': 'START'
            }
        3.6.2 Dừng lại
            Data request format:
            {
                'Action': 'STOP'
            }
        3.6.3 Xuất
            Data request format:
            {
                'Action': 'PRINT'
            }
    3.7 Copy File
        File: ./Controls/FileControl.py
        Method: DIRECTORY
        Chức năng này để truyền file giữa client và server

        3.7.1 Xuất dictionary tree
            Data request format:
            {
                'Action': 'SHOW'
            }
            
        3.7.2 Copy file từ client đến server
            Data request format:
            {
                'Action': 'COPYTO'
                'Root': '' //Đường dẫn để copy
            }
        
        3.7.3 Copy file từ client đến server
            Data request format:
            {
                'Action': 'COPY'
                'Root': '' //Đường dẫn file copy
            }
        
        3.7.4 Xóa file ở server
            Data request format:
            {
                'Action': 'DEL'
                'Root': '' //Đường dẫn file cần xóa
            }
    3.8 Điều kiển Webcam
        File: ./Controls/WebcamRecordControl.py
        Method: WEBCAMRECORD
        Chức năng này để điều kiển Webcam trên máy tính, quay video lưu xuống rồi zip gửi mail

        3.8.1 Bắt đầu
            Data request format:
            {
                'Action': 'START'
            }
        3.8.2 Ngưng và xuất gửi mail
            Data request format:
            {
                'Action': 'STOP'
            }

            


