import argparse
import math

parser = argparse.ArgumentParser(description="Loan Calculator")
parser.add_argument("--type")
parser.add_argument("--principal", type=float, default=0)
parser.add_argument("--payment", type=float, default=0)
parser.add_argument("--periods", type=float, default=0)
parser.add_argument("--interest", type=float, default=0)
args = parser.parse_args()


def check_accuracy(operation_type, principal, payment, periods, interest):
    accuracy = True
    args_list = []
    if principal > 0:
        args_list.append(principal)
    if payment > 0:
        args_list.append(payment)
    if periods > 0:
        args_list.append(periods)
    if len(args_list) < 2:
        accuracy = False
    if operation_type != "diff" and operation_type != "annuity":
        accuracy = False
    if not interest or interest < 0:
        accuracy = False
    if operation_type == "diff" and (not principal or not periods):
        accuracy = False

    return accuracy


def get_str_result(months):
    months = math.ceil(months)
    y_str = ""
    m_str = ""
    put_and = ""
    y = months // 12
    m = months % 12

    if y == 1:
        y_str = "1 year"
    elif y:
        y_str = f"{y} years"
    if m == 1:
        m_str = "1 month"
    elif m:
        m_str = f"{m} months"
    if m and y:
        put_and = " and "

    return f"It will take {y_str}{put_and}{m_str} to repay this loan!"


def main():
    operation_type = args.type
    principal = args.principal
    payment = args.payment
    periods = args.periods
    nominal = args.interest/1200

    accurate = check_accuracy(operation_type, principal, payment, periods, nominal)

    if accurate:
        hole_payment = 0
        if not principal:
            second_part = nominal * math.pow((nominal + 1), periods)
            third_part = math.pow((nominal + 1), periods) - 1
            principal = payment / (second_part / third_part)
            if operation_type == "annuity":
                print(f"Your loan principal = {int(principal)}!")
        if not payment:
            second_part = nominal * math.pow((nominal + 1), periods)
            third_part = math.pow((nominal + 1), periods) - 1
            payment = principal * (second_part / third_part)
            if operation_type == "annuity":
                print(f"Your annuity payment = {math.ceil(payment)}!")
        if not periods:
            periods = math.log(payment / (payment - principal * nominal), (nominal + 1))
            string_result = get_str_result(periods)
            if operation_type == "annuity":
                print(string_result)
        if operation_type == "diff":
            for i in range(1, int(periods)+1):
                diff = math.ceil(principal / periods + nominal * (principal - principal * (i - 1) / periods))
                hole_payment += diff
                print(f"Month {i}: payment in {diff}")
            print()

        if operation_type == "annuity":
            hole_payment = math.ceil(periods) * math.ceil(payment)

        print(f"Overpayment = {math.ceil(hole_payment - principal)}")

    else:
        print("Incorrect parameters")


main()
