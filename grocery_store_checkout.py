from tkinter import *
import pandas as pd
import io

def get_sum(products_info, orders):
	tot = 0
	for i, amount in orders.items():
		if amount != 0:
			tot += float(products_info['prix'][i].replace(',', '.'))
	return tot

def write_orders(products_info, orders):
	outFile = io.open('orders.txt', mode='a', encoding='utf-8')
	for i, amount in orders.items():
		outFile.write(products_info['produits'][i] + '\t' + str(amount) + '\n')
	outFile.close()

def get_orders_summary(products_info):
	try:
		orders = {}
		inFile = io.open('orders.txt', mode='r', encoding='utf-8')
		line = inFile.readline()
		while line != '':
			elm = line.strip().split('\t')
			if elm[0] not in orders.keys():
				orders[elm[0]] = int(elm[1])
			else:
				orders[elm[0]] += int(elm[1])
			line = inFile.readline()
		inFile.close()
	except:
		orders = {}
	txt = ''
	for prod, amount in orders.items():
		txt += prod + ' : ' + str(amount) + ' - '
	if txt != '':
		txt = txt[:len(txt)-2]
		return txt
	else:
		return ''

def costumer_window(main_window, products_info):
	# Main frame: for every costumer, we clean the window so we delete this frame.
	main_f = Frame(main_window, width=1000, height=1000, borderwidth=5)
	main_f.pack(fill=BOTH)
	# Show the order summary
	txt = get_orders_summary(products_info)
	summary = Label(main_f, text=txt)
	summary.pack()
	spinboxes = []
	for i in products_info.index:
		# Get product and information
		prod = products_info['produits'][i]
		price = products_info['prix'][i]
		max_amount = products_info['quantite_max'][i]

		# 1. Create the frame for the current product
		f = Frame(main_f, width=1000, height=1000, borderwidth=5)
		f.pack(fill=BOTH)
		txt = prod + ' (' + str(price) + ' €)'
		n = Label(f, text=txt)
		n.pack(side="left", fill=X)

		# 2. Choose the amount
		q = StringVar()
		q.set(0)
		s = Spinbox(f, from_=0, to=100, increment=1, width=2)
		s.config(textvariable=q, font="sans 24", justify="center")
		s.pack(side="right", fill=X)
		spinboxes.append((i, s))

	# Total button
	var = IntVar()
	total_button = Button(main_f, text="Valider", command=lambda: var.set(1))
	total_button.pack()
	total_button.wait_variable(var) # Wait till the button is pressed
	orders = {s[0]: int(s[1].get()) for s in spinboxes}
	write_orders(products_info, orders)
	txt = 'Total commande : ' + str(get_sum(products_info, orders)) + ' €'
	n = Label(main_f, text=txt)
	n.pack(side='bottom')

	return main_f

main_window = Tk()
main_window.title('ADAK')

l0 = Label(main_window, text="-------------------------------------------------------")
l1 = Label(main_window, text="Association Des Amis de Kerdehel")
l2 = Label(main_window, text="-------------------------------------------------------")
for l in [l0, l1, l2]: l.pack()

products_info = pd.read_csv('stock_products.csv')

button_quit_pressed = False
while True:
	frame = costumer_window(main_window, products_info)
	# New costumer button
	var = IntVar()
	new_costumer_button = Button(frame, text="Client suivant", command=lambda: var.set(1))
	new_costumer_button.pack()
	new_costumer_button.wait_variable(var)

	# Clearing the page
	for widget in frame.winfo_children():
		widget.destroy()
	frame.destroy()
	

main_window.mainloop()