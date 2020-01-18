from flask import Flask, render_template, url_for, flash, request, redirect
from inventory import app
from flask_sqlalchemy import SQLAlchemy
from inventory.forms import ProductForm, LocationForm, ProductMovementForm
from inventory.models import Product, Location, ProductMovement
from inventory import db
from functools import reduce



@app.route('/about')
def about():
    return render_template('home.html')

@app.route('/products')
def products():
	products = Product.query.all()
	if len(products) != 0:
		return render_template('products.html', title='Product', products=products)
	else:
		flash('No Products present in the inventory system. Add Product')

@app.route('/add_product', methods=["POST", "GET"])
def add_product():
	form=ProductForm()
	if request.method=="POST" and form.validate():
		product_id=Product(name=form.name.data)
		db.session.add(product_id)
		db.session.commit()
		flash('Entered Product ID added!', 'success')
		return redirect(url_for('products'))
	return render_template('add_product.html', form=form)


@app.route('/edit_product/<string:id>', methods=['GET', 'POST'])
def edit_product(id):
	product_name=Product.query.filter_by(id=id).first()
	form=ProductForm()
	form.name.data=product_name.name
	if request.method=="POST" and form.validate():
		product_name.name=request.form["name"]
		db.session.commit()
		flash('Updated Product ID', 'success')
		return redirect(url_for('products'))
	return render_template('edit_product.html', form=form)


@app.route('/delete_product/<string:id>', methods=['POST'])
def delete_product(id):
	import ipdb; ipdb.set_trace();
	print(id)
	product_name=Product.query.get(id)
	db.session.delete(product_name)
	db.session.commit()
	flash('Delete Product ID', 'success')
	form=ProductForm()
	products=Products.query.all()
	return render_template('products.html', title='Product', products=products)


@app.route('/locations')
def locations():
	locations = Location.query.all()
	if len(locations) != 0:
		return render_template('location.html', title='Location', locations=locations)
	else:
		flash('No Location present in the inventory. Add Location')

@app.route('/edit_location/<string:id>', methods=['GET', 'POST'])
def edit_location(id):
	form=LocationForm()
	product_location=Location.query.get(id)
	form.name.data=product_location.name
	if request.method=="POST" and form.validate():
		product_location.name=request.form["name"]
		db.session.commit()
		flash('Updated Product Location', 'success')
		return redirect(url_for('locations'))
	return render_template('edit_location.html', form=form)	

@app.route('/add_location', methods=["POST", "GET"])
def add_location():
	form=LocationForm()
	if request.method=="POST" and form.validate():
		location_id = Location(name=form.name.data)
		db.session.add(location_id)
		db.session.commit()
		flash('Entered Location ID added!', 'success')
		return redirect(url_for('locations'))
	return render_template('add_location.html', title='Add Location', form=form)

@app.route('/productmovement')
def product_movement():
	product_movements = ProductMovement.query.all()
	if len(product_movements) != 0:
		return render_template('productmovement.html', title='Product Movement', 
			product_movements=product_movements)
	else:
		flash('No Product Movement has taken place.')

@app.route('/add_productmovement', methods=["POST", "GET"])
def add_product_movement():
	form=ProductMovementForm()
	products=Product.query.all()
	locations = Location.query.all()
	form.from_location.choices = [(location.id,location.name) for location in locations]
	form.from_location.choices.append((' ',"--"))
	form.to_location.choices = [(location.id,location.name) for location in locations]
	form.to_location.choices.append((' ',"--"))
	form.product_id.choices = [(product.id,product.name) for product in products]
	if request.method=="POST" and form.validate():
		from_location = Location.query.get(form.from_location.data)
		to_location = Location.query.get(form.to_location.data)
		product_id = Product.query.get(form.product_id.data)
		quantity = form.quantity.data
        # TODO data validation, from_location, to_location cannot be empty
		data = ProductMovement(from_location_id=from_location, 
			                   to_location_id=to_location,
			                   product_id=product_id, 
			                   quantity=form.quantity.data)
		db.session.add(data)
		db.session.commit()
		flash('Product Movement Details added', 'success')
		return redirect(url_for('product_movement'))
	return render_template('add_productmovement.html', title='Add Product Movement', form=form)

@app.route('/edit_productmovement/<int:id>', methods=['GET', 'POST'])
def edit_productmovement(id):
	product_movement=ProductMovement.query.get(id)
	print(product_movement.from_location.name)
	form=ProductMovementForm()
	products=Product.query.all()
	locations = Location.query.all()
	form.from_location.choices = [(location.id,location.name) for location in locations]
	form.from_location.choices.append((' ',"--"))
	form.to_location.choices = [(location.id,location.name) for location in locations]
	form.to_location.choices.append((' ',"--"))
	form.product_id.choices = [(product.id,product.name) for product in products]
	form.from_location.default=product_movement.from_location.id
	form.to_location.default=product_movement.to_location.id if product_movement.to_location != None else ' '
	form.product_id.default=product_movement.product.id 
	form.quantity.default=product_movement.quantity
	form.process()
	
	if request.method=="POST" and form.validate():
		product_movement.to_location=Location.query.get(request.form["to_location"])
		product_movement.from_location=Location.query.get(request.form["from_location"])
		product_movement.product_id=Product.query.get(request.form["product_id"])
		product_movement.quantity=request.form["quantity"]
		db.session.commit()
		flash('Updated Product Movement', 'success')
		return redirect(url_for('product_movement'))
	return render_template('edit_productmovement.html', form=form)	



@app.route('/dashboard')
def dashboard():
	D = {}
	total_product_quantities = {}
	locations=Location.query.all()
	for location in locations:
		D[location.name] = {}  
		product_locations=ProductMovement.query.filter_by(to_location_id=location.id).all()
		for product_location in product_locations:
			if product_location.product.name not in D[location.name]:
				D[location.name].update({product_location.product.name: [product_location.quantity]})
			else:
				D[location.name][product_location.product.name].append(product_location.quantity)
	for product_location in D:
		total_product_quantities[product_location] = {}
		for product_details in D[product_location]:
			if len(D[product_location][product_details]) > 1:
				total_product_quantities[product_location][product_details] = sum(D[product_location][product_details])
			else:
				total_product_quantities[product_location][product_details] = D[product_location][product_details][0]
	return render_template('dashboard.html', title='Dashboard', product_details=total_product_quantities)
