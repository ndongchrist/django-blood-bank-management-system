from global_data.enums import BloodTypes, GenderType, UserTypes, Status

def site_info(request):
    return {
        'blood_Choices':BloodTypes.choices,
        'gender_choices': GenderType.choices,
        'DONOR': UserTypes.choices[0][0],
        'PATIENT': UserTypes.choices[1][0],
        'status': Status.choices,
    }