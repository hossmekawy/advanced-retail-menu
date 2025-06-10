# -*- coding: utf-8 -*-
"""
مسارات نظام نقاط البيع - POS System Routes
"""
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from datetime import datetime
from decimal import Decimal
from i18n import _
from admin.forms import PaymentForm, RefundForm, InvoiceForm, CashTransactionForm, ShiftForm, CloseShiftForm
from models import Order, Payment, Invoice, CashDrawer, CashTransaction, Shift, User
from extensions import db


def init_pos_routes(bp):
    """تهيئة مسارات نظام نقاط البيع - Initialize POS routes"""
    
    @bp.route('/pos')
    @login_required
    def pos_dashboard():
        """لوحة تحكم نقاط البيع - POS dashboard"""
        # الحصول على الوردية النشطة - Get active shift
        active_shift = Shift.query.filter_by(user_id=current_user.id, status='active').first()
        
        # إحصائيات اليوم - Today's statistics
        today = datetime.now().date()
        today_orders = Order.query.filter(
            db.func.date(Order.created_at) == today
        ).count()
        
        today_payments = Payment.query.filter(
            db.func.date(Payment.payment_timestamp) == today,
            Payment.payment_status == 'completed'
        ).count()
        
        today_revenue = db.session.query(
            db.func.sum(Payment.amount)
        ).filter(
            db.func.date(Payment.payment_timestamp) == today,
            Payment.payment_status == 'completed'
        ).scalar() or 0
        
        # الحصول على خزنة النقد - Get cash drawer
        cash_drawer = CashDrawer.get_default_drawer()
        
        # الطلبات المعلقة للدفع - Pending payment orders
        pending_orders = Order.query.filter_by(payment_status='unpaid').limit(10).all()
        
        return render_template('admin/pos/dashboard.html',
                             active_shift=active_shift,
                             today_orders=today_orders,
                             today_payments=today_payments,
                             today_revenue=today_revenue,
                             cash_drawer=cash_drawer,
                             pending_orders=pending_orders)

    @bp.route('/pos/payment/<int:order_id>', methods=['GET', 'POST'])
    @login_required
    def pos_process_payment(order_id):
        """معالجة الدفع - Process payment"""
        order = Order.query.get_or_404(order_id)
        form = PaymentForm()
        
        # تعيين المبلغ الافتراضي - Set default amount
        if request.method == 'GET':
            form.amount.data = order.total_amount
        
        if form.validate_on_submit():
            # التحقق من صحة المبلغ - Validate amount
            if form.amount.data > order.total_amount:
                flash(_('مبلغ الدفع أكبر من إجمالي الطلب'), 'error')
                return render_template('admin/pos/payment.html', order=order, form=form)
            
            # إنشاء الدفع - Create payment
            payment = Payment(
                order_id=order.id,
                amount=form.amount.data,
                payment_method=form.payment_method.data,
                payment_status='completed',
                processed_by_user_id=current_user.id,
                reference_number=form.reference_number.data,
                notes=form.notes.data
            )
            payment.payment_number = payment.generate_payment_number()
            
            db.session.add(payment)
            
            # تحديث حالة الدفع للطلب - Update order payment status
            total_paid = db.session.query(
                db.func.sum(Payment.amount)
            ).filter_by(order_id=order.id, payment_status='completed').scalar() or 0
            
            total_paid += form.amount.data
            
            if total_paid >= order.total_amount:
                order.payment_status = 'paid'
            else:
                order.payment_status = 'partial'
            
            # إضافة معاملة نقدية إذا كان الدفع نقداً - Add cash transaction if cash payment
            if form.payment_method.data == 'cash':
                cash_drawer = CashDrawer.get_default_drawer()
                cash_drawer.add_transaction(
                    amount=form.amount.data,
                    transaction_type='sale',
                    description=f'دفع الطلب {order.order_number}',
                    user_id=current_user.id,
                    reference_id=order.id
                )
            
            db.session.commit()
            
            flash(_('تم معالجة الدفع بنجاح'), 'success')
            return redirect(url_for('admin.pos_payment_receipt', payment_id=payment.id))
        
        return render_template('admin/pos/payment.html', order=order, form=form)

    @bp.route('/pos/payment/<int:payment_id>/receipt')
    @login_required
    def pos_payment_receipt(payment_id):
        """إيصال الدفع - Payment receipt"""
        payment = Payment.query.get_or_404(payment_id)
        return render_template('admin/pos/receipt.html', payment=payment)

    @bp.route('/pos/refund/<int:payment_id>', methods=['GET', 'POST'])
    @login_required
    def pos_process_refund(payment_id):
        """معالجة الاسترداد - Process refund"""
        payment = Payment.query.get_or_404(payment_id)
        form = RefundForm()
        
        # تعيين المبلغ الافتراضي - Set default amount
        if request.method == 'GET':
            form.amount.data = payment.amount
        
        if form.validate_on_submit():
            # التحقق من صحة المبلغ - Validate amount
            if form.amount.data > payment.amount:
                flash(_('مبلغ الاسترداد أكبر من مبلغ الدفع'), 'error')
                return render_template('admin/pos/refund.html', payment=payment, form=form)
            
            # إنشاء دفع الاسترداد - Create refund payment
            refund = Payment(
                order_id=payment.order_id,
                amount=-form.amount.data,  # مبلغ سالب للاسترداد - Negative amount for refund
                payment_method=payment.payment_method,
                payment_status='completed',
                processed_by_user_id=current_user.id,
                notes=f'استرداد للدفع {payment.payment_number}: {form.reason.data}'
            )
            refund.payment_number = refund.generate_payment_number()
            
            db.session.add(refund)
            
            # تحديث حالة الدفع الأصلي - Update original payment status
            if form.amount.data == payment.amount:
                payment.payment_status = 'refunded'
            
            # تحديث حالة دفع الطلب - Update order payment status
            order = payment.order
            total_paid = db.session.query(
                db.func.sum(Payment.amount)
            ).filter_by(order_id=order.id, payment_status='completed').scalar() or 0
            
            if total_paid <= 0:
                order.payment_status = 'unpaid'
            elif total_paid < order.total_amount:
                order.payment_status = 'partial'
            else:
                order.payment_status = 'paid'
            
            # إضافة معاملة نقدية إذا كان الدفع نقداً - Add cash transaction if cash payment
            if payment.payment_method == 'cash':
                cash_drawer = CashDrawer.get_default_drawer()
                cash_drawer.add_transaction(
                    amount=form.amount.data,
                    transaction_type='refund',
                    description=f'استرداد للطلب {order.order_number}',
                    user_id=current_user.id,
                    reference_id=order.id
                )
            
            db.session.commit()
            
            flash(_('تم معالجة الاسترداد بنجاح'), 'success')
            return redirect(url_for('admin.order_detail', id=order.id))
        
        return render_template('admin/pos/refund.html', payment=payment, form=form)

    @bp.route('/pos/invoice/<int:order_id>', methods=['GET', 'POST'])
    @login_required
    def pos_generate_invoice(order_id):
        """إنشاء فاتورة - Generate invoice"""
        order = Order.query.get_or_404(order_id)
        form = InvoiceForm()
        
        if form.validate_on_submit():
            # إنشاء الفاتورة - Create invoice
            invoice = Invoice(
                order_id=order.id,
                tax_rate=form.tax_rate.data or 0,
                created_by_user_id=current_user.id,
                notes=form.notes.data
            )
            invoice.invoice_number = invoice.generate_invoice_number()
            # تمرير الطلب إلى دالة حساب المجاميع - Pass order to calculate totals function
            invoice.calculate_totals(order)

            db.session.add(invoice)
            db.session.commit()
            
            flash(_('تم إنشاء الفاتورة بنجاح'), 'success')
            return redirect(url_for('admin.pos_invoice_detail', invoice_id=invoice.id))
        
        return render_template('admin/pos/invoice_form.html', order=order, form=form)

    @bp.route('/pos/invoice/<int:invoice_id>')
    @login_required
    def pos_invoice_detail(invoice_id):
        """تفاصيل الفاتورة - Invoice details"""
        invoice = Invoice.query.get_or_404(invoice_id)
        return render_template('admin/pos/invoice.html', invoice=invoice)

    @bp.route('/pos/invoice/<int:invoice_id>/pdf')
    @login_required
    def pos_invoice_pdf(invoice_id):
        """فاتورة PDF - PDF invoice"""
        invoice = Invoice.query.get_or_404(invoice_id)
        
        # هنا يمكن إضافة مكتبة PDF مثل reportlab أو weasyprint
        # Here you can add PDF library like reportlab or weasyprint
        
        # للآن، سنعيد توجيه إلى صفحة الفاتورة - For now, redirect to invoice page
        return redirect(url_for('admin.pos_invoice_detail', invoice_id=invoice_id))

    @bp.route('/pos/cash')
    @login_required
    def pos_cash_management():
        """إدارة النقد - Cash management"""
        cash_drawer = CashDrawer.get_default_drawer()
        
        # آخر المعاملات - Recent transactions
        recent_transactions = CashTransaction.query.filter_by(
            cash_drawer_id=cash_drawer.id
        ).order_by(CashTransaction.created_at.desc()).limit(20).all()
        
        return render_template('admin/pos/cash.html',
                             cash_drawer=cash_drawer,
                             recent_transactions=recent_transactions)

    @bp.route('/pos/cash/transaction', methods=['GET', 'POST'])
    @login_required
    def pos_cash_transaction():
        """معاملة نقدية - Cash transaction"""
        form = CashTransactionForm()
        
        if form.validate_on_submit():
            cash_drawer = CashDrawer.get_default_drawer()
            
            # إضافة المعاملة - Add transaction
            transaction = cash_drawer.add_transaction(
                amount=form.amount.data,
                transaction_type=form.transaction_type.data,
                description=form.description.data,
                user_id=current_user.id
            )
            
            if form.notes.data:
                transaction.notes = form.notes.data
            
            db.session.commit()
            
            flash(_('تم تسجيل المعاملة بنجاح'), 'success')
            return redirect(url_for('admin.pos_cash_management'))
        
        return render_template('admin/pos/cash_transaction.html', form=form)

    @bp.route('/pos/shift/start', methods=['GET', 'POST'])
    @login_required
    def pos_start_shift():
        """بدء وردية - Start shift"""
        # التحقق من عدم وجود وردية نشطة - Check no active shift
        active_shift = Shift.query.filter_by(user_id=current_user.id, status='active').first()
        if active_shift:
            flash(_('لديك وردية نشطة بالفعل'), 'warning')
            return redirect(url_for('admin.pos_dashboard'))

        form = ShiftForm()
        cash_drawer = CashDrawer.get_default_drawer()

        # تعيين الرصيد الحالي كافتراضي - Set current balance as default
        if request.method == 'GET':
            form.opening_balance.data = cash_drawer.current_balance

        if form.validate_on_submit():
            # إنشاء وردية جديدة - Create new shift
            shift = Shift(
                user_id=current_user.id,
                cash_drawer_id=cash_drawer.id,
                opening_balance=form.opening_balance.data,
                notes=form.notes.data
            )
            shift.shift_number = shift.generate_shift_number()

            db.session.add(shift)
            db.session.commit()

            flash(_('تم بدء الوردية بنجاح'), 'success')
            return redirect(url_for('admin.pos_dashboard'))

        return render_template('admin/pos/start_shift.html', form=form, cash_drawer=cash_drawer)

    @bp.route('/pos/shift/close', methods=['GET', 'POST'])
    @login_required
    def pos_close_shift():
        """إغلاق وردية - Close shift"""
        # الحصول على الوردية النشطة - Get active shift
        active_shift = Shift.query.filter_by(user_id=current_user.id, status='active').first()
        if not active_shift:
            flash(_('لا توجد وردية نشطة'), 'warning')
            return redirect(url_for('admin.pos_dashboard'))

        form = CloseShiftForm()
        cash_drawer = CashDrawer.get_default_drawer()

        if form.validate_on_submit():
            # إغلاق الوردية - Close shift
            active_shift.close_shift(
                closing_balance=form.closing_balance.data,
                notes=form.notes.data
            )

            # تحديث رصيد الخزنة - Update cash drawer balance
            cash_drawer.current_balance = form.closing_balance.data
            cash_drawer.last_updated_by_user_id = current_user.id

            db.session.commit()

            flash(_('تم إغلاق الوردية بنجاح'), 'success')
            return redirect(url_for('admin.pos_shift_report', shift_id=active_shift.id))

        return render_template('admin/pos/close_shift.html',
                             form=form,
                             shift=active_shift,
                             cash_drawer=cash_drawer)

    @bp.route('/pos/shift/<int:shift_id>/report')
    @login_required
    def pos_shift_report(shift_id):
        """تقرير الوردية - Shift report"""
        shift = Shift.query.get_or_404(shift_id)

        # التحقق من الصلاحية - Check permission
        if shift.user_id != current_user.id:
            flash(_('غير مصرح لك بعرض هذا التقرير'), 'error')
            return redirect(url_for('admin.pos_dashboard'))

        return render_template('admin/pos/shift_report.html', shift=shift)

    @bp.route('/pos/shifts')
    @login_required
    def pos_shifts_list():
        """قائمة الورديات - Shifts list"""
        page = request.args.get('page', 1, type=int)

        shifts = Shift.query.filter_by(user_id=current_user.id).order_by(
            Shift.created_at.desc()
        ).paginate(page=page, per_page=20, error_out=False)

        return render_template('admin/pos/shifts.html', shifts=shifts)

    @bp.route('/pos/print-receipt/<int:payment_id>')
    @login_required
    def pos_print_receipt(payment_id):
        """طباعة الإيصال - Print receipt"""
        payment = Payment.query.get_or_404(payment_id)

        # إنشاء إيصال حراري - Create thermal receipt
        response = make_response(render_template('admin/pos/thermal_receipt.html', payment=payment))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'

        return response
