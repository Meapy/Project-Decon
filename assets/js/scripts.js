
$('.register').click(function (event) {
    event.preventDefault();
    var name = $('#nameRegister').val();
    var email = $('#emailRegister').val();
    var password = $('#passwordRegister').val();
    $.ajax({
        url: '/users/register',
        type: 'POST',
        data: {
            name: name,
            email: email,
            password: password
        },
        success: function(data) {
            if (data.error) {
                alert(data.message);
            } else {
                alert("sucessfuly registered, you can login in now");
                window.location.href = '/';
            }
        }
    });
});
$('.login').click(function (event) {
    event.preventDefault();
    var email = $('#emailLogin').val();
    var password = $('#passwordLogin').val();
    $.ajax({
        url: '/users/login',
        type: 'POST',
        data: {
            email: email,
            password: password
        },
        success: function (data) {
            if (data.error) {
                alert(data.message);
                console.log("failure", data);
            } else {
                console.log("success", data);
                window.location.href = '/';
            }
        }
    });
}
);
//script to send data to the server using ajax and post method
/*Date of Birth, City of Birth, Email, Address, 
Gender, Hobbies, Civil state, Profession, Salary per year, 
upload a picture, and favourite sport */
$(".saveData").click(function (event) {
    event.preventDefault();
    var name = $("input[name='name']").val();
    var email = $("input[name='email']").val();
    var dob = $("input[name='birthday']").val();
    var city = $("input[name='city']").val();
    var address = $("input[name='address']").val();
    var gender = $("input[name='gender']").val();
    var hobbies = $("input[name='hobbies']").val();
    var civilS = $("input[name='civilS']").val();
    var job = $("input[name='job']").val();
    var salary = $("input[name='salary']").val();
    var sport = $("input[name='sport']").val();
    var picture = $("input[name='picture']").val();
    var data = {
        name: name,
        email: email,
        dob: dob,
        city: city,
        address: address,
        gender: gender,
        hobbies: hobbies, 
        civilS: civilS, 
        job: job, 
        salary: salary, 
        picture: picture,
        sport: sport,
    }
    $.ajax({
        url: '/users/update',
        type: 'POST',
        data: data,
        success: function (data) {
            if (data.error) {
                alert(data.message);
                console.log("failure", data);
            } else {
                alert("data has been updated");
                console.log("success", data);
                //window.location.href = '/';
            }
        }
    });
});




