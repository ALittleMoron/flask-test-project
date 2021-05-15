import re
from flask import Blueprint, render_template, redirect, url_for, request
from .forms import ElgamalForm
from .validators import validate_keys
from models import EncryptedResult, DecryptedResult
from app import db


elgamal = Blueprint('elgamal', __name__, template_folder='templates',
                    static_folder='static')


@elgamal.route('/')
def elgamal_index():
    return redirect(url_for('elgamal.elgamal_encrypt'))


@elgamal.route('/encrypt/', methods=['GET', 'POST'])
def elgamal_encrypt():
    if request.method == 'POST':
        is_skip = False
        keys, message = request.form.get('keys'), request.form.get('message')
        if not keys or not message:
            error = f'Вы не ввели ключи или сообщение в форму...\nВаши данные: {keys, message}'
            is_skip = True
        
        row_keys = keys
        for x in range(int(len(keys)**0.5)+1):
            keys = keys.replace(' ', '')
            standart_parse = keys
        if not is_skip:
            parsed_keys = list(map(int, standart_parse.split(',')))
        else:
            parsed_keys = []

        keys = re.findall(r'\d+', keys)
        keys = list(map(int, keys))
        if parsed_keys != keys and not is_skip:
            is_skip = True
            error = f'Вы ввели некорректные ключи. Не все значения - числа.'

        if not is_skip:
            is_valid, error = validate_keys(keys)
            if not is_valid:
                is_skip = True

        if not is_skip:
            if request.form.get('checkElgamalEncrypt') and request.form.get('checkElgamalDecrypt'):
                pub, priv = list(map(str, keys[:3])), list(map(str, keys[3:]))
                pub, priv = ', '.join(pub), ', '.join(priv)
                
                encrypt = EncryptedResult(public_keys=pub, result=message)
                decrypt = DecryptedResult(private_keys=priv, result=message)
                db.session.add(encrypt)
                db.session.add(decrypt)
                db.session.commit()

                return redirect(
                    url_for(
                        'elgamal.elgamal_encrypt_and_decrypt_result',
                        enc_slug=encrypt.slug,
                        dec_slug=decrypt.slug
                        )
                    )
            elif request.form.get('checkElgamalEncrypt'):
                encrypt = EncryptedResult(public_keys=row_keys, result=message)
                db.session.add(encrypt)
                db.session.commit()

                return redirect(
                    url_for(
                        'elgamal.elgamal_encrypt_result',
                        enc_slug=encrypt.slug
                        )
                    )
            elif request.form.get('checkElgamalDecrypt'):
                decrypt = DecryptedResult(private_keys=row_keys, result=message)
                db.session.add(decrypt)
                db.session.commit()
                
                return redirect(
                    url_for(
                        'elgamal.elgamal_decrypt_result',
                        dec_slug=decrypt.slug
                        )
                    )
            else:
                error = 'Вы не выбрали действия (шифровка и/или дешифровка)'
        
        return render_template(
            'elgamal/elgamal_form.html',
            title='Схема Эль-Гамаля',
            form=ElgamalForm(),
            error=error
            )
    
    return render_template(
        'elgamal/elgamal_form.html', 
        title='Схема Эль-Гамаля',
        form=ElgamalForm()
        )


@elgamal.route('/result/<slug>')
def elgamal_result(slug):
    result = EncryptedResult.query.filter(EncryptedResult.slug==slug).first()
    return render_template('elgamal/elgamal_result.html', result=result)


@elgamal.route('/encrypt-result/<enc_slug>')
def elgamal_encrypt_result(enc_slug):
    result = EncryptedResult.query.filter(EncryptedResult.slug==enc_slug).first()
    return render_template('elgamal/elgamal_result.html', result=result)


@elgamal.route('/decrypt-result/<dec_slug>')
def elgamal_decrypt_result(dec_slug):
    result = DecryptedResult.query.filter(DecryptedResult.slug==dec_slug).first()
    return render_template('elgamal/elgamal_result.html', result=result)


@elgamal.route('/full-result/<enc_slug>-<dec_slug>')
def elgamal_encrypt_and_decrypt_result(enc_slug, dec_slug):
    enc_result = EncryptedResult.query.filter(EncryptedResult.slug==enc_slug).first()
    dec_result = DecryptedResult.query.filter(DecryptedResult.slug==dec_slug).first()
    print(enc_result, dec_result)
    return render_template('elgamal/elgamal_result.html', enc=enc_result, dec=dec_result)